from wagtail import blocks
from wagtail.models import Page


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)
    text = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)

    def bulk_to_python(self, values):
        page_ids = (value.get("page") for value in values)

        pages = Page.objects.in_bulk(page_ids)

        for value in values:
            page_id = value.get("page")
            if page_id is not None:
                value["page"] = pages[page_id]

        return values


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


class MenuStreamBlock(blocks.StreamBlock):
    submenu = SubmenuBlock()
