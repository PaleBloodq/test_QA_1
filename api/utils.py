import os
from datetime import datetime, timedelta
import uuid
from rest_framework.request import Request
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
from api import models

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


def decode_token(token: str) -> models.Profile | None:
    try:
        decoded = jwt.decode(token, public_key, ['RS256'])
        telegram_id = decoded.get('telegram_id')
        token_expiraton = decoded.get('token_expiraton')
        token_seed = decoded.get('token_seed')
        if telegram_id and token_expiraton and token_seed:
            token_expiraton = datetime.fromisoformat(token_expiraton)
            profile = models.Profile.get_or_none(telegram_id=telegram_id)
            if (
                profile
                and token_seed == profile.token_seed.hex
                and token_expiraton >= datetime.now()
            ):
                return profile
    except:
        pass
