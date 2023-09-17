import random
import re

from django.conf import settings
from django.contrib.sites.models import Site


def generate_username(name=None, last_name=None, second_last_name=None) -> str:
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    value = ""
    max_range = 33
    if name is not None and last_name is not None and second_last_name is not None:
        value = re.sub("[\W_]+", "", name + last_name + second_last_name)[:16]  # noqa
        max_range = 17
    for _val in range(1, max_range):
        character_position = round(random.random() * 61)
        value += characters[character_position]
    return value


def get_current_site_front():
    current_site = Site.objects.get_current()
    if settings.IS_DEV:
        return "http://127.0.0.1:3080"
    else:
        return f"https://{current_site.domain}"
