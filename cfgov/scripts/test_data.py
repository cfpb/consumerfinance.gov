from django.contrib.auth.models import User

from wagtail.core.blocks import StreamValue

from scripts import _atomic_helpers as atomic

from v1.models import (
    BlogPage, BrowseFilterablePage, BrowsePage, SublandingFilterablePage
)
from v1.models.snippets import ReusableText
from v1.tests.wagtail_pages.helpers import publish_changes, publish_page


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


def add_reusable_text_snippet(slug, cls):
    snippet_with_heading = ReusableText(
        title='Test reusable text snippet with sidefoot heading',
        sidefoot_heading='Test sidefoot heading',
        text='A reusable snippet with a sidefoot heading',
    )
    snippet_without_heading = ReusableText(
        title='Test reusable text snippet without a sidefoot heading',
        text='A reusable snippet without a sidefoot heading.',
    )
    snippet_with_heading.save()
    snippet_without_heading.save()
    full_width_text = {
        'type': 'full_width_text',
        'value': [
            {
                'type': 'reusable_text',
                'value': snippet_with_heading.id
            },
            {
                'type': 'reusable_text',
                'value': snippet_without_heading.id
            }
        ]
    }
    page = cls(
        title=slug,
        slug=slug,
    )
    page.content = StreamValue(
        page.content.stream_block,
        [full_width_text],
        True,
    )
    publish_page(page)


def add_feedback_form(slug, cls):
    feedback_form = {
        'type': 'feedback',
        'value': []
    }
    page = cls(
        title=slug,
        slug=slug,
    )
    page.content = StreamValue(
        page.content.stream_block,
        [feedback_form],
        True,
    )
    publish_page(page)


def run():
    add_filterable_page(
        slug='sfp',
        cls=SublandingFilterablePage,
    )
    add_filterable_page(
        slug='bfp',
        cls=BrowseFilterablePage,
    )
    add_reusable_text_snippet(
        slug='rts',
        cls=BrowsePage,
    )
    add_feedback_form(
        slug='feedback',
        cls=BrowsePage,
    )
    user = User.objects.filter(username='admin')
    if user:
        user.first().delete()
    User.objects.create_superuser(
        username='admin',
        password='password',
        email=''
    )
