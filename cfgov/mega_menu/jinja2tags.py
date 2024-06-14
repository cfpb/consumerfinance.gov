from django.conf import settings
from django.db import models

from jinja2 import pass_context
from jinja2.ext import Extension

from mega_menu.models import Menu


def select_menu_for_context(context):
    # Choose a menu for a view context.
    # First try "language" from the context, if it is defined.
    # Otherwise fall back to the default Django language.
    context_language = context.get("language")
    default_language = settings.LANGUAGE_CODE[:2]
    languages = [context_language, default_language]

    return (
        Menu.objects.filter(language__in=languages)
        .annotate(
            menu_sort_order=models.Case(
                models.When(language=context_language, then=0),
                models.When(language=default_language, then=1),
                output_field=models.IntegerField(),
            )
        )
        .order_by("menu_sort_order")
        .first()
    )


def get_mega_menu_content(context):
    menu = select_menu_for_context(context)

    if not menu:
        return None

    return menu.get_content_for_frontend(request=context.get("request"))


class MegaMenuExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update(
            {
                "get_mega_menu_content": pass_context(get_mega_menu_content),
            }
        )
