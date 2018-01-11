from wagtail.wagtailcore import hooks

from v1.models.snippets import MenuItem

@hooks.register('before_serve_shared_page')
def before_serve_shared_page(page, request, args, kwargs):
    request.show_draft_megamenu = True

def get_menu_items(request):
    show_draft = hasattr(request, 'show_draft_megamenu')
    return [item.get_content(show_draft)
            for item in MenuItem.objects.all().order_by('order')]
