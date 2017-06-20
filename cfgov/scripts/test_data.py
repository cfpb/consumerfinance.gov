from django.contrib.auth.models import User

from wagtail.wagtailcore.blocks import StreamValue

from v1.models import SublandingFilterablePage, BrowseFilterablePage, BlogPage
from v1.tests.wagtail_pages.helpers import publish_page, publish_changes

from scripts import _atomic_helpers as atomic


def add_children(parent, num, slug):
    for i in range(num):
        child = parent.add_child(
            instance=BlogPage(
                title="{} child {}".format(slug, i),
                slug="{}-child-{}".format(slug, i)
            )
        )
        child.tags.add(u'tag{}'.format(i))
        child.tags.add(u'shared-tag')
        publish_changes(child)


def add_filterable_page(slug, cls):
    filterable_page = cls(
        title=slug,
        slug=slug,
    )
    filterable_page.content = StreamValue(
        filterable_page.content.stream_block,
        [atomic.filter_controls],
        True
    )
    publish_page(filterable_page)
    add_children(
        parent=filterable_page,
        num=11,
        slug=slug,
    )


def run():
    add_filterable_page(
        slug='sfp',
        cls=SublandingFilterablePage,
    )
    add_filterable_page(
        slug='bfp',
        cls=BrowseFilterablePage,
    )

    user = User.objects.filter(username='admin')
    if user:
        user.first().delete()
    User.objects.create_superuser(
        username='admin',
        password='password',
        email=''
    )
