from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from treebeard.mp_tree import MP_Node


def get_page(apps, slug):
    base_page_cls = apps.get_model('wagtailcore', 'Page')
    return base_page_cls.objects.get(slug=slug)


def get_free_path(apps, parent_page):
    offset = 1
    base_page_cls = apps.get_model('wagtailcore', 'Page')

    while True:
        path = MP_Node._get_path(
            parent_page.path,
            parent_page.depth + 1,
            parent_page.numchild + offset
        )

        try:
            base_page_cls.objects.get(path=path)
        except base_page_cls.DoesNotExist:
            return path

        offset += 1


@transaction.atomic
def get_or_create_page(apps, page_cls_app, page_cls_name, title, slug,
                       parent_page, live=False, shared=False, **kwargs):
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
        path=get_free_path(apps, parent_page),
        content_type=page_content_type,
        live=live,
        shared=shared,
        **kwargs
    )

    parent_page.numchild += 1
    parent_page.save()

    return page
