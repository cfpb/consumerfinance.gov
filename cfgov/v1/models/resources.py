from django.core.validators import URLValidator
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class ResourceTag(TaggedItemBase):
    content_object = ParentalKey('v1.Resource', related_name='tagged_items')


class TaggableSnippetManager(models.Manager):
    def filter_by_tags(self, tags):
        snippets = self.all()
        for tag in tags or []:
            snippets = snippets.filter(tags__name__iexact=tag)

        return snippets


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

    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Resources will be listed alphabetically by title in a '
        'Resource List module, unless any in the list have a number in this '
        'field; those with an order value will appear in ascending order.'
    )

    tags = TaggableManager(
        through=ResourceTag,
        blank=True,
        help_text='Tags can be used to filter resources in a Resource List.'
    )

    objects = TaggableSnippetManager()

    panels = [
        FieldPanel('title'),
        FieldPanel('desc'),
        ImageChooserPanel('thumbnail'),
        DocumentChooserPanel('related_file'),
        DocumentChooserPanel('alternate_file'),
        FieldPanel('link'),
        FieldPanel('alternate_link'),
        FieldPanel('order'),
        FieldPanel('tags'),
    ]

    # Makes fields available to the Actions chooser in a Resource List module
    resource_list_field_choices = [
        ('related_file', 'Related file'),
        ('alternate_file', 'Alternate file'),
        ('link', 'Link'),
        ('alternate_link', 'Alternate link'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order', 'title',)
