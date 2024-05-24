import os
from datetime import datetime, timedelta
from hashlib import md5
import uuid

import requests
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
from api import models, serializers

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


def hash_product_publication(product_id: int, title: str, platforms: list[str]):
    to_hash = f'{product_id} {title} {platforms}'
    return md5(to_hash.encode('utf-8')).hexdigest()


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