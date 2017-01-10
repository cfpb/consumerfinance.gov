import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailsnippets.models import register_snippet

from ..atomic_elements import molecules


@register_snippet
class Contact(models.Model):
    heading = models.CharField(verbose_name=('Heading'), max_length=255,
                               help_text=("The snippet heading"))
    body = RichTextField(blank=True)

    hash = models.CharField(max_length=32, editable=False)

    contact_info = StreamField([
        ('email', molecules.ContactEmail()),
        ('phone', molecules.ContactPhone()),
        ('address', molecules.ContactAddress()),
    ], blank=True)

    panels = [
        FieldPanel('heading'),
        FieldPanel('body'),
        StreamFieldPanel('contact_info'),
    ]

    def __str__(self):
        return self.heading

    @classmethod
    def get_by_title_slug(self, title, slug):
        return self.objects.get(
            hash=hashlib.md5(title + ';;' + slug).hexdigest())


@receiver(pre_save, sender=Contact)
def set_hash(sender, instance, **kwargs):
    heading = instance.heading
    instance.hash = hashlib.md5(heading).hexdigest()

    if ';;' in instance.heading:
        heading = instance.heading.split(';;')[0]

    instance.heading = heading
