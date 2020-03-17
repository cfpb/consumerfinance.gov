from itertools import chain

from wagtail.core import blocks
from wagtail.core.models import Page


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)
    text = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)


class LinkWithIconBlock(LinkBlock):
    icon = blocks.CharBlock()


class SubmenuColumnBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    links = blocks.ListBlock(LinkBlock(), default=[])


class SubmenuBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    overview_page = blocks.PageChooserBlock(required=False)
    featured_links = blocks.ListBlock(LinkBlock(), default=[])
    other_links = blocks.ListBlock(LinkWithIconBlock(), default=[])
    columns = blocks.ListBlock(SubmenuColumnBlock(), default=[])

    def bulk_to_python(self, values):
        """Support bulk page retrieval to reduce database queries."""
        page_ids = set(chain(*map(self.get_referenced_page_ids, values)))
        pages = Page.objects.in_bulk(page_ids)

        for value in values:
            self.replace_referenced_page_ids_with_pages(value, pages)

        return [blocks.StructValue(self, value) for value in values]

    def get_referenced_page_ids(self, value):
        """Collect all page IDs referenced by this block."""
        page_ids = list()

        # The submenu overview page.
        page_ids.append(value.get('overview_page'))

        # Any pages in featured, other, and column links.
        page_ids.extend(link.get('page') for link in self.link_iterator(value))

        # Return the unique set of non-null page IDs.
        return set(page_id for page_id in page_ids if page_id is not None)

    def replace_referenced_page_ids_with_pages(self, value, pages):
        """Replace page ID references with Page instances."""
        # The submenu overview page.
        if 'overview_page' in value:
            value['overview_page'] = pages.get(value['overview_page'])

        # Any pages in featured, other, and column links.
        for link in self.link_iterator(value):
            if 'page' in link:
                link['page'] = pages.get(link['page'])

    def link_iterator(self, value):
        return chain(
            value.get('featured_links') or [],
            value.get('other_links') or [],
            chain(*(
                (column.get('links') or [])
                for column in (value.get('columns') or [])
            ))
        )


class MenuStreamBlock(blocks.StreamBlock):
    submenu = SubmenuBlock()
