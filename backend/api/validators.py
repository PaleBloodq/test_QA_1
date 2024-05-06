import logging
import re
import requests
from django.core.exceptions import ValidationError
from urllib.parse import urljoin


def validate_ps_store_url(value):
    if not value.endswith('/'):
        value = f"{value}/"

    url_pattern = re.compile(r'^https://store.playstation.com/.+/concept/\d+/')
    if not url_pattern.match(value):
        raise ValidationError("Неверный формат URL-адреса PlayStation Store.")

    modified_url = re.sub(r'^https://store.playstation.com/.*?/',
                          'https://store.playstation.com/en-tr/', value)
    response = requests.get(modified_url,allow_redirects=True)


    if modified_url != response.url:
        raise ValidationError("URL-адрес PlayStation Store недействителен.")

    return modified_url

