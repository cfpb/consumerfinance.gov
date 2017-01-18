import hashlib

from django.core.validators import URLValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
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


class ResourceTag(TaggedItemBase):
    content_object = ParentalKey('v1.Resource', related_name='tagged_items')


class TaggableSnippetManager(models.Manager):
    def filter_by_tags(self, tags):
        snippets = self.all()
        for tag in tags or []:
            snippets = snippets.filter(tags__name=tag)

        return snippets


@register_snippet
class Resource(ClusterableModel):
    title = models.CharField(max_length=255)
    desc = RichTextField(verbose_name='Description', blank=True)

    thumbnail = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    related_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    alternate_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    link = models.URLField(
        blank=True,
        help_text='Example: URL to order a few copies of a printed piece.',
        validators=[URLValidator]
    )

    alternate_link = models.URLField(
        blank=True,
        help_text='Example: a URL to for ordering bulk copies.',
        validators=[URLValidator]
    )

    tags = TaggableManager(through=ResourceTag, blank=True)

    hash = models.CharField(max_length=32, editable=False)

    objects = TaggableSnippetManager()

    panels = [
        FieldPanel('title'),
        FieldPanel('desc'),
        ImageChooserPanel('thumbnail'),
        DocumentChooserPanel('related_file'),
        DocumentChooserPanel('alternate_file'),
        FieldPanel('link'),
        FieldPanel('alternate_link'),
        FieldPanel('tags'),
    ]

    def template(self, is_single=False):
        # check if single or not, return concatenation of subtype and kind of
        # template
        if is_single:
            return self.subtype + '-single.html'
        else:
            return self.subtype + '-list-item.html'

    def __str__(self):
        return self.title

    @classmethod
    def get_by_title_slug(self, title, slug):
        return self.objects.get(hash=hashlib.md5(title + ';;' + slug).hexdigest())


@receiver(pre_save, sender=Contact)
def set_hash(sender, instance, **kwargs):
    heading = instance.heading
    instance.hash = hashlib.md5(heading).hexdigest()

    if ';;' in instance.heading:
        heading = instance.heading.split(';;')[0]

    instance.heading = heading
