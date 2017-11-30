from v1.models.snippets import MenuItem
from flags.template_functions import flag_enabled


def get_menu_items(request):
    show_draft = flag_enabled('DRAFT_MENU', request)
    return [item.get_content(show_draft)
            for item in MenuItem.objects.all().order_by('order')]
