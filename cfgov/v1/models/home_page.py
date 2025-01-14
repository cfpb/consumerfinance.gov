from wagtail.admin.panels import ObjectList, TabbedInterface
from wagtail.models import Page

from v1.models.base import CFGOVPage


class HomePage(CFGOVPage):
    edit_handler = TabbedInterface(
        [
            # This is required to support editing of the page's title field.
            # HomePages have no other Wagtail-editable content fields.
            ObjectList(Page.content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/home_page/home_page.html"
