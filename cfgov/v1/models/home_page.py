from wagtail.admin.panels import ObjectList, TabbedInterface
from wagtail.models import Page

from flags.state import flag_enabled

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

    def get_template(self, request, *args, **kwargs):
        try:
            if flag_enabled("SPANISH_HOMEPAGE"):
                return {
                    "en": "v1/home_page/home_page.html",
                    "es": "v1/home_page/home_page.html",
                }[self.language]
            else:
                return {
                    "en": "v1/home_page/home_page.html",
                    "es": "v1/home_page/home_page_legacy.html",
                }[self.language]
        except KeyError as e:
            raise NotImplementedError(
                f"Unsupported HomePage language: {self.language}"
            ) from e
