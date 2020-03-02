from django.conf import settings
from django.utils.translation import get_language_from_request

from jinja2 import contextfunction
from jinja2.ext import Extension

from mega_menu.models import Menu


def select_menu_for_context(context):
    language = context.get('language')

    if not language:
        request = context['request']
        language = get_language_from_request(request, check_path=True)

    # First try to find a menu for the language from the context.
    try:
        return Menu.objects.get(language=language[:2])
    except Menu.DoesNotExist:
        pass

    # Next try to find a menu for the default Django language.
    try:
        return Menu.objects.get(language=settings.LANGUAGE_CODE[:2])
    except Menu.DoesNotExist:
        pass

    # If we can't find a menu, return None.
    return None


def get_mega_menu_content(context):
    menu = select_menu_for_context(context)

    if not menu:
        return None

    return menu.get_content_for_frontend(request=context.get('request'))


class MegaMenuExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'get_mega_menu_content': contextfunction(get_mega_menu_content),
        })
