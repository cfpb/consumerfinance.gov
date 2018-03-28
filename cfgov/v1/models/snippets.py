from django.core.validators import URLValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from v1.atomic_elements import molecules
# We import ReusableTextChooserBlock here because this is where it used to
# live. That caused circular imports when it was imported into models. It's no
# longer imported into models from this file, but there are migrations which
# still look for it here.
from v1.blocks import ReusableTextChooserBlock  # noqa


@python_2_unicode_compatible
@register_snippet
class ReusableText(index.Indexed, models.Model):
    title = models.CharField(
        verbose_name='Snippet title (internal only)',
        max_length=255
    )
    sidefoot_heading = models.CharField(
        blank=True,
        max_length=255,
        help_text='Applies "slug" style heading. '
                  'Only for use in sidebars and prefooters '
                  '(the "sidefoot"). See '
                  '[GHE]/flapjack/Modules-V1/wiki/Atoms#slugs'
    )
    text = RichTextField()

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('sidefoot_heading', partial_match=True),
        index.SearchField('text', partial_match=True),
    ]

    def __str__(self):
        return self.title


@python_2_unicode_compatible
@register_snippet
class Contact(models.Model):
    heading = models.CharField(verbose_name=('Heading'), max_length=255,
                               help_text=("The snippet heading"))
    body = RichTextField(blank=True)

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


class ResourceTag(TaggedItemBase):
    content_object = ParentalKey('v1.Resource', related_name='tagged_items')


class TaggableSnippetManager(models.Manager):
    def filter_by_tags(self, tags):
        snippets = self.all()
        for tag in tags or []:
            snippets = snippets.filter(tags__name=tag)

        return snippets


@python_2_unicode_compatible
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

    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Snippets will be listed alphabetically by title in a '
        'Snippet List module, unless any in the list have a number in this '
        'field; those with an order value will appear in ascending order.'
    )

    tags = TaggableManager(
        through=ResourceTag,
        blank=True,
        help_text='Tags can be used to filter snippets in a Snippet List.'
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

    # Makes fields available to the Actions chooser in a Snippet List module
    snippet_list_field_choices = [
        ('related_file', 'Related file'),
        ('alternate_file', 'Alternate file'),
        ('link', 'Link'),
        ('alternate_link', 'Alternate link'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order', 'title')
