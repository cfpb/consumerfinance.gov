from wagtail.wagtailcore.blocks import StreamValue

from v1.models import SublandingFilterablePage, BlogPage
from v1.tests.wagtail_pages.helpers import publish_page

from scripts import _atomic_helpers as atomic


# Create a sublanding filterable page & its children if it doesn't exist already
try:
    sfp = SublandingFilterablePage.objects.get(slug='sfp')
except SublandingFilterablePage.DoesNotExist:
    sfp = SublandingFilterablePage(
        title='sfp',
        slug='sfp'
    )
    # sfp.content = StreamValue(
    #     sfp.content.stream_block,
    #     [atomic.filter_controls],
    #     True
    # )
    publish_page(child=sfp)

    # Add a child
    sfp.add_child(instance=BlogPage(title="sfp child", slug="sfp-child"))
