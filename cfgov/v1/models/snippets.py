from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey

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
    term_en = models.CharField(
        max_length=255,
    )
    term_es = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    definition_en = RichTextField(
        null=True,
        blank=True
    )
    definition_es = RichTextField(
        null=True,
        blank=True
    )
    answer_page_en = models.ForeignKey(
        'ask_cfpb.AnswerPage',
        related_name='glossary_terms',
        null=True,
        blank=True
    )
    answer_page_es = models.ForeignKey(
        'ask_cfpb.AnswerPage',
        related_name='glossary_terms_es',
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
        index.SearchField('term_en', partial_match=True),
        index.SearchField('definition_en', partial_match=True),
        index.SearchField('term_es', partial_match=True),
        index.SearchField('definition_es', partial_match=True),
    ]

    def term(self, language='en'):
        if language == 'es':
            return self.term_es
        return self.term_en

    def definition(self, language='en'):
        if language == 'es':
            return self.definition_es
        return self.definition_en

    def answer_page_url(self, language='en'):
        if language == 'es':
            return self.answer_page_es.url
        return self.answer_page_en.url

    def anchor(self, language='en'):
        return slugify(self.term(language))

    def __str__(self):
        return self.term_en
