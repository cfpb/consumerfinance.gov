from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

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


@python_2_unicode_compatible
@register_snippet
class RelatedResource(index.Indexed, models.Model):
    title = models.CharField(
        max_length=255
    )
    text = RichTextField()

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('text', partial_match=True),
    ]

    def __str__(self):
        return self.title


@python_2_unicode_compatible
@register_snippet
class GlossaryTerm(index.Indexed, models.Model):
    term = models.CharField(
        max_length=255,
    )
    definition = RichTextField()
    anchor = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    term_es = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    definition_es = RichTextField(
        null=True,
        blank=True
    )
    portal_topic = ParentalKey(
        'v1.PortalTopic',
        related_name='glossary_terms',
        null=True,
        blank=True
    )

    search_fields = [
        index.SearchField('term', partial_match=True),
        index.SearchField('definition', partial_match=True),
    ]

    def __str__(self):
        return self.term

    def clean(self):
        super(GlossaryTerm, self).clean()
        if not self.anchor:
            self.anchor = slugify(self.term)