from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


def get_page(apps, slug):
    base_page_cls = apps.get_model('wagtailcore', 'Page')
    return base_page_cls.objects.get(slug=slug)


def make_path_string(base_path='', child_number=0):
    if child_number > 14:
        # This function uses hex formatting as a shortcut so only supports
        # up to 15 children (1-F), as Wagtail (and Treebeard) appear to skip
        # 0 and use '0001' as the first path. Larger number of children use
        # non-hex letters (such as '000G') and more complex formatting will
        # be needed here for those cases.
        raise ValueError('unsupported format')

    return base_path + '000{:x}'.format(child_number + 1).upper()


@transaction.atomic
def get_or_create_page(apps, page_cls_app, page_cls_name, title, slug,
                       parent_page, live=False, shared=False):
    try:
        return get_page(apps, slug)
    except ObjectDoesNotExist:
        pass

    ContentType = apps.get_model('contenttypes.ContentType')
    page_cls = apps.get_model(page_cls_app, page_cls_name)

    page_content_type = ContentType.objects.get_for_model(page_cls)

    parent_page = get_page(apps, slug=parent_page.slug)

    page = page_cls.objects.create(
        title=title,
        slug=slug,
        depth=parent_page.depth + 1,
        path=make_path_string(parent_page.path, parent_page.numchild),
        content_type=page_content_type,
        live=live,
        shared=shared
    )

    parent_page.numchild += 1
    parent_page.save()

    return page
