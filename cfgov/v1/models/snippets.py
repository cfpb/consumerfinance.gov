from django.db import models

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from . import molecules


@register_snippet
class Contact(models.Model):
    title = models.CharField(verbose_name=('Title'), max_length=255,
                             help_text=("The snippet title as you'd like it to be seen by the public"))
    slug = models.SlugField(verbose_name=('Slug'), max_length=255,
                            help_text=("The name of the snippet as it will appear in URLs " +
                                        "e.g http://domain.com/blog/[my-slug]/"))
    body = RichTextField(blank=True)
    contact_info = StreamField([
        ('email', molecules.ContactEmail()),
        ('phone', molecules.ContactPhone()),
        ('address', molecules.ContactAddress()),
    ], blank=True)

    web_label = models.CharField(verbose_name=('Website Label'), max_length=255, blank=True)
    web_url = models.CharField(verbose_name=('Website'), max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        StreamFieldPanel('contact_info'),
        FieldPanel('web_label'),
        FieldPanel('web_url'),
    ]

    def __str__(self):
        return self.title
