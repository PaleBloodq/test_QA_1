import logging
import os
from typing import Optional
from datetime import datetime, timedelta
from hashlib import md5
import uuid
from decimal import Decimal

import requests
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
from asgiref.sync import async_to_sync
from api import models, serializers
from api.senders import send_admin_notification, NotifyLevels
from ps_store_api import models as ps_models

BOT_URL = f'http://{os.environ.get("TELEGRAM_BOT_HOST")}:{os.environ.get("TELEGRAM_BOT_PORT")}/api/order/change/'

with open(os.environ.get('RSA_PEM_FILE'), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )


with open(os.environ.get('RSA_PUB_FILE'), "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )


def get_ip(request: Request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def encode_profile(telegram_id: int) -> str:
    profile, created = models.Profile.objects.get_or_create(
        telegram_id=telegram_id
    )
    token_expiraton = datetime.now() + timedelta(hours=5)
    profile.token_seed = uuid.uuid4()
    profile.save()
    return jwt.encode({
        'telegram_id': profile.telegram_id,
        'token_expiraton': token_expiraton.isoformat(),
        'token_seed': profile.token_seed.hex,
    }, private_key, 'RS256')


def decode_token(token: str, check_profile_only: bool = False) -> models.Profile | None:
    try:
        decoded = jwt.decode(token, public_key, ['RS256'])
        telegram_id = decoded.get('telegram_id')
        token_expiraton = decoded.get('token_expiraton')
        token_seed = decoded.get('token_seed')
        if telegram_id and token_expiraton and token_seed:
            profile = models.Profile.get_or_none(telegram_id=telegram_id)
            if check_profile_only:
                return profile
            if token_seed == profile.token_seed.hex and datetime.fromisoformat(token_expiraton) >= datetime.now():
                return profile
    except:
        pass


def auth_required(func):
    def wrapped(self, request: Request):
        if request.META.get('HTTP_AUTHORIZATION'):
            token = request.META.get('HTTP_AUTHORIZATION').removeprefix('Bearer ')
            profile = decode_token(token)
            if profile:
                return func(self, request, profile)
        return Response(status=status.HTTP_403_FORBIDDEN)
    return wrapped


def check_promo_code(profile: models.Profile, promo_code: str | None) -> int | None:
    if promo_code:
        promo = models.PromoCode.objects.filter(
            promo_code=promo_code,
            expiration__gte=datetime.now()
        ).first()
        if promo and not models.Order.objects.filter(profile=profile, promo_code=promo_code):
            return promo.discount

def send_order_to_bot(order: models.Order):
    requests.post(BOT_URL, json=serializers.OrderSerializer(order).data)


def normalize_price(price: Optional[Decimal], exchange: bool = False) -> Optional[Decimal]:
    if price:
        if exchange:
            if price <= 899:
                exchange_rate = Decimal(5.0)
            elif 900 <= price <= 1699:
                exchange_rate = Decimal(4.5)
            else:
                exchange_rate = Decimal(4.0)
            price *= exchange_rate
        if price >= 1000 and price % 1000 < 25:
            price -= price % Decimal(1000) + Decimal(5)
        price = price - price % Decimal(5)
    return price


def update_sales_leaders(order: models.Order):
    for product in models.OrderProduct.objects.filter(order=order):
        publication = models.Publication.objects.filter(id=product.product_id).first() \
            or models.AddOn.objects.filter(id=product.product_id).first() \
            or models.Subscription.objects.filter(id=product.product_id).first()
        if publication:
            publication.product.orders += 1
            publication.product.save()
    current_leaders = models.Tag.objects.get(database_name='leaders').products
    actual_leaders = models.Product.objects.order_by('-orders')[:30]
    for product in current_leaders.all():
        if product not in actual_leaders:
            current_leaders.remove(product)
    for product in actual_leaders:
        if product not in current_leaders.all():
            current_leaders.add(product)


def update_product(product: models.Product, ps_concept: ps_models.Concept):
    if product.ps_concept != ps_concept:
        product.ps_concept = ps_concept
    if product.parse_release_date:
        product.release_date = ps_concept.release_date
    product.save()
    return product


def update_publication(publication: models.Publication | models.AddOn):
    if isinstance(publication, models.Publication):
        ps_product = publication.ps_product
        if publication.parse_release_date:
            publication.release_date = ps_product.release_date
        if publication.product.release_date is None:
            publication.product.release_date = publication.release_date
            publication.product.save()
    if isinstance(publication, models.AddOn):
        ps_product = publication.ps_add_on
    if publication.parse_title:
        publication.title = ps_product.name
    if publication.parse_price:
        price = normalize_price(ps_product.price.discounted_price, True)
        if publication.final_price != price:
            async_to_sync(send_admin_notification)({
                'text': f'Цена на издание товара {publication.product.title} изменилась',
                'level': NotifyLevels.WARN.value,
            })
            publication.price_changed = True
        publication.final_price = price
        publication.discount = ps_product.price.discount
        publication.discount_deadline = ps_product.price.discount_deadline
    if publication.parse_ps_plus_price and ps_product.ps_plus_price:
        ps_plus_price = normalize_price(ps_product.ps_plus_price.discounted_price, True)
        if publication.ps_plus_final_price != price:
            async_to_sync(send_admin_notification)({
                'text': f'Цена на издание товара {publication.product.title} изменилась',
                'level': NotifyLevels.WARN.value,
            })
            publication.price_changed = True
        publication.ps_plus_final_price = ps_plus_price
        publication.ps_plus_discount = ps_product.ps_plus_price.discount
        publication.ps_plus_discount_deadline = ps_product.ps_plus_price.discount_deadline
    if publication.parse_image:
        if not all((publication.product_page_image, publication.search_image, publication.offer_image)):
            publication.set_photo_from_url(ps_product.portrait_image)
    publication.save()
    if publication.parse_platforms:
        for platform in ps_product.platforms.all():
            platform = models.Platform.objects.get_or_create(name=platform.name)[0]
            publication.platforms.add(platform)
