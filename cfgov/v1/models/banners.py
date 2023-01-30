from django.core.validators import RegexValidator
from django.db import models
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

from v1.atomic_elements.molecules import Notification


class BannerContent(StreamBlock):
    content = Notification()

    class Meta:
        block_counts = {
            "content": {"min_num": 1, "max_num": 1},
        }


class Banner(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="For internal reference only; does not appear on the site.",
    )
    url_pattern = models.CharField(
        max_length=1000,
        verbose_name="URL patterns",
        help_text=mark_safe(
            "A regular expression pattern for matching URLs "
            "that should show the banner, for example: "
            "<code>contact-us|^/complaint/$</code>"
        ),
        validators=[RegexValidator(regex=r"[A-Za-z0-9\-_.:/?&|\^$]")],
    )
    # TODO: Add `min_num` and `max_num` arguments of 1 to the StreamField
    # and eliminate the BannerContent StreamBlock
    # if https://github.com/wagtail/wagtail/pull/5185 ever gets merged.
    content = StreamField(BannerContent, use_json_field=True)

    enabled = models.BooleanField()

    panels = [
        FieldPanel("title"),
        FieldPanel("url_pattern"),
        FieldPanel("content"),
        FieldPanel("enabled"),
    ]

    def __str__(self):
        return self.title
