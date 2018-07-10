from v1.models.menu_item import MenuItem


def get_menu_items(request):
    '''
    Assembles mega menu content based on draft state.
    The 'show_draft_megamenu' attribute is set to True
    for sharing sites in 'before_serve_shared_page' hook.
    '''
    show_draft = hasattr(request, 'show_draft_megamenu')

    return [item.get_content(show_draft)
            for item in MenuItem.objects.all().order_by('order')]
