from wagtail.snippets.views.snippets import SnippetViewSet

from mega_menu.models import Menu


class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "list-ul"
    menu_label = "Mega menu"
    add_to_admin_menu = True
