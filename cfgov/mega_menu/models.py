from operator import itemgetter

from django.conf import settings
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from mega_menu.blocks import MenuStreamBlock
from mega_menu.frontend_conversion import FrontendConverter


class Menu(models.Model):
    language = models.CharField(
        choices=sorted(settings.LANGUAGES, key=itemgetter(1)),
        max_length=100,
        primary_key=True,
    )

    submenus = StreamField(MenuStreamBlock())

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
