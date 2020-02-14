from django.conf import settings
from django.template import loader
from django.utils.translation import get_language_from_request

from flags.state import flag_enabled
from jinja2 import Markup, contextfunction
from jinja2.ext import Extension

from mega_menu.frontend_conversion import FrontendConverter
from mega_menu.models import Menu


def mega_menu_template(context):
    request = context.get('request')

    if flag_enabled('MEGA_MENU_VAR_1', request=request):
        return '_includes/organisms/mega-menu-var-1.html'
    else:
        return '_includes/organisms/mega-menu.html'


def select_menu_for_context(context):
    language = context.get('language')

    if not language:
        request = context['request']
        language = get_language_from_request(request, check_path=True)

    try:
        return Menu.objects.get(language=language[:2])
    except Menu.DoesNotExist:
        return Menu.objects.get(language=settings.LANGUAGE_CODE[:2])


def mega_menu(context):
    frontend_converter = FrontendConverter(
        select_menu_for_context(context),
        request=context.get('request')
    )

    new_context = context.get_all()
    new_context['menu_items'] = frontend_converter.get_menu_items()

    template = loader.get_template(mega_menu_template(context))
    return Markup(template.render(new_context))


class MegaMenuExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'mega_menu': contextfunction(mega_menu),
            'mega_menu_template': contextfunction(mega_menu_template),
        })
