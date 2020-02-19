from itertools import chain


try:
    from wagtail.core import blocks
    from wagtail.core.models import Page
    from wagtail.images import get_image_model
    from wagtail.images.blocks import ImageChooserBlock
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore import blocks
    from wagtail.wagtailcore.models import Page
    from wagtail.wagtailimages import get_image_model
    from wagtail.wagtailimages.blocks import ImageChooserBlock


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)
    text = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)


class FeaturedLinkBlock(LinkBlock):
    body = blocks.CharBlock()
    image = ImageChooserBlock()


class LinkWithIconBlock(LinkBlock):
    icon = blocks.CharBlock()


class SubmenuColumnBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    links = blocks.ListBlock(LinkBlock(), default=[])


class SubmenuBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    overview_page = blocks.PageChooserBlock(required=False)
    featured_links = blocks.ListBlock(FeaturedLinkBlock(), default=[])
    other_links = blocks.ListBlock(LinkWithIconBlock(), default=[])
    columns = blocks.ListBlock(SubmenuColumnBlock(), default=[])

    def bulk_to_python(self, values):
        """Support bulk page retrieval to reduce database queries."""
        page_ids = set(chain(*map(self.get_referenced_page_ids, values)))
        pages = Page.objects.in_bulk(page_ids)

        image_ids = set(chain(*map(self.get_referenced_image_ids, values)))
        images = get_image_model().objects.in_bulk(image_ids)

        for value in values:
            self.replace_referenced_page_ids_with_pages(value, pages)
            self.replace_referenced_image_ids_with_images(value, images)

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

    def get_referenced_image_ids(self, value):
        """Collect all image IDs referenced by this block."""
        image_ids = [
            link.get('image') for link in value.get('featured_links') or []
        ]

        # Return the unique set of non-null image IDs.
        return set(image_id for image_id in image_ids if image_id is not None)

    def replace_referenced_image_ids_with_images(self, value, images):
        """Replace image ID references with image instances."""
        for featured_link in value.get('featured_links') or []:
            if 'image' in featured_link:
                featured_link['image'] = images.get(featured_link['image'])


class MenuStreamBlock(blocks.StreamBlock):
    submenu = SubmenuBlock()
