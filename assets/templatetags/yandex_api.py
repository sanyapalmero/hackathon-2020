from django.conf import settings
from django.template import Library


register = Library()


@register.simple_tag
def get_yandex_maps_api_key():
    return settings.YANDEX_MAPS_API_KEY
