from operator import itemgetter

from django.conf import settings
from django.db import models
from django.utils import translation

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import PreviewableMixin

from mega_menu.blocks import MenuStreamBlock
from mega_menu.frontend_conversion import FrontendConverter


class Menu(PreviewableMixin, models.Model):
    language = models.CharField(
        choices=sorted(settings.LANGUAGES, key=itemgetter(1)),
        max_length=100,
        primary_key=True,
    )

    submenus = StreamField(
        MenuStreamBlock(),
    )

    class Meta:
        ordering = ("language",)

    panels = [
        FieldPanel("language"),
        FieldPanel("submenus"),
    ]

    def __str__(self):
        return str(dict(settings.LANGUAGES)[self.language])

    def get_content_for_frontend(self, request=None):
        return FrontendConverter(self, request=request).get_menu_items()

    def get_preview_template(self, request, mode_name):
        return "mega_menu/preview.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name=mode_name)
        context.update(
            {
                "current_language": self.language,
                "get_mega_menu_content": self.get_content_for_frontend,
            }
        )
        return context

    def serve_preview(self, request, mode_name):
        with translation.override(self.language):
            response = super().serve_preview(request, mode_name=mode_name)

            # Need to render the response while our translation is active.
            return response.render()
