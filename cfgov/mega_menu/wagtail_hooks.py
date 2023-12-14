from wagtail.snippets.models import register_snippet

from mega_menu.views import MenuViewSet


register_snippet(MenuViewSet)
