from django.contrib.auth.models import User

from wagtail.wagtailcore.blocks import StreamValue

from v1.models import SublandingFilterablePage, BlogPage
from v1.tests.wagtail_pages.helpers import publish_page, publish_changes

from scripts import _atomic_helpers as atomic


def add_children(parent, num):
    for i in range(num):
        child = parent.add_child(
            instance=BlogPage(
                title="sfp child {}".format(i),
                slug="sfp-child-{}".format(i)
            )
        )
        child.tags.add(u'tag{}'.format(i))
        child.tags.add(u'shared-tag')
        publish_changes(child)


def run():
    sfp = SublandingFilterablePage.objects.filter(slug='sfp')
    if not sfp:
        sfp = SublandingFilterablePage(
            title='sfp',
            slug='sfp'
        )
        sfp.content = StreamValue(
            sfp.content.stream_block,
            [atomic.filter_controls],
            True
        )
        publish_page(sfp)

        add_children(parent=sfp, num=10)

    user = User.objects.filter(username='admin')
    if user:
        user.first().delete()
    User.objects.create_superuser(
        username='admin',
        password='password',
        email=''
    )
