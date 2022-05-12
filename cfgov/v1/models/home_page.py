from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.core.models import Page

from v1.models.base import CFGOVPage


def image_passthrough(image, *args, **kwargs):
    """Passthrough replacement for Wagtail {{ image }} tag.

    This is needed because, as written, the hero module template assumes that
    it will get passed a Wagtail image object, which needs to get converted
    into e.g. a URL to render. We want to pass the hero module a URL directly.
    """
    return image


def image_alt_value_passthrough(image, *args, **kwargs):
    """Passthrough replacement for v1.jinja2tags.image_alt_value.

    This is needed because, as written, the info unit template assumes that it
    will get passed a Wagtail image object. We want to pass a dict which
    contains the various image properties, including alt text, if defined.
    """
    return image.get("alt", "")


class HomePage(CFGOVPage):
    edit_handler = TabbedInterface(
        [
            # This is required to support editing of the page's title field.
            # HomePages have no other Wagtail-editable content fields.
            ObjectList(Page.content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            {
                "image_passthrough": image_passthrough,
                "image_alt_value_passthrough": image_alt_value_passthrough,
            }
        )
        return context

    def get_template(self, request, *args, **kwargs):
        try:
            return {
                "en": "v1/home_page/home_page.html",
                "es": "v1/home_page/home_page_legacy.html",
            }[self.language]
        except KeyError as e:
            raise NotImplementedError(
                f"Unsupported HomePage language: {self.language}"
            ) from e
