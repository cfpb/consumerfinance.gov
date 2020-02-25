from django.conf import settings
from django.db import models

from mega_menu.blocks import MenuStreamBlock


try:
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.core.fields import StreamField
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.wagtailcore.fields import StreamField


class Menu(models.Model):
    language = models.CharField(
        choices=settings.LANGUAGES,
        max_length=2,
        primary_key=True
    )

    submenus = StreamField(MenuStreamBlock())

    class Meta:
        ordering = ('language',)

    panels = [
        FieldPanel('language'),
        StreamFieldPanel('submenus'),
    ]

    def __str__(self):
        return str(dict(settings.LANGUAGES)[self.language])
