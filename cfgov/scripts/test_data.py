from django.contrib.auth.models import User

from wagtail.wagtailcore.blocks import StreamValue

from v1.models import SublandingFilterablePage, BlogPage
from v1.tests.wagtail_pages.helpers import publish_page, publish_changes

from scripts import _atomic_helpers as atomic


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

        # Add a child
        child = sfp.add_child(
            instance=BlogPage(title="sfp child", slug="sfp-child")
        )
        child.tags.add(u'tag1')
        child.tags.add(u'tag2')
        publish_changes(child)

    user = User.objects.filter(username='admin')
    if user:
        user.first().delete()
    User.objects.create_superuser(
        username='admin',
        password='password',
        email=''
    )
