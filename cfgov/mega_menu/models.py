from django.conf import settings
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from mega_menu.blocks import MenuStreamBlock
from mega_menu.frontend_conversion import FrontendConverter


class Menu(models.Model):
    language = models.CharField(
        choices=settings.LANGUAGES, max_length=2, primary_key=True
    )

    submenus = StreamField(MenuStreamBlock())

    class Meta:
        ordering = ("language",)

    panels = [
        FieldPanel("language"),
        StreamFieldPanel("submenus"),
    ]

    def __str__(self):
        return str(dict(settings.LANGUAGES)[self.language])

    def get_content_for_frontend(self, request=None):
        return FrontendConverter(self, request=request).get_menu_items()
