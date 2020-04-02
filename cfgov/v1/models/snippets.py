from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from v1.atomic_elements import molecules
# We import ReusableTextChooserBlock here because this is where it used to
# live. That caused circular imports when it was imported into models. It's no
# longer imported into models from this file, but there are migrations which
# still look for it here.
from v1.blocks import ReusableTextChooserBlock  # noqa


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


@register_snippet
class Contact(models.Model):
    heading = models.CharField(verbose_name=('Heading'), max_length=255,
                               help_text=("The snippet heading"))
    body = RichTextField(blank=True)
    body_shown_in_expandables = models.BooleanField(default=False)

    contact_info = StreamField([
        ('email', molecules.ContactEmail()),
        ('phone', molecules.ContactPhone()),
        ('address', molecules.ContactAddress()),
        ('hyperlink', molecules.ContactHyperlink()),
    ], blank=True)

    panels = [
        FieldPanel('heading'),
        FieldPanel('body'),
        FieldPanel('body_shown_in_expandables'),
        StreamFieldPanel('contact_info'),
    ]

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['heading']


@register_snippet
class RelatedResource(index.Indexed, models.Model):
    title = models.CharField(max_length=255)
    title_es = models.CharField(max_length=255, blank=True, null=True)
    text = RichTextField(blank=True, null=True)
    text_es = RichTextField(blank=True, null=True)

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('text', partial_match=True),
        index.SearchField('title_es', partial_match=True),
        index.SearchField('text_es', partial_match=True),
    ]

    def trans_title(self, language='en'):
        if language == 'es':
            return self.title_es or ''
        return self.title or ''

    def trans_text(self, language='en'):
        if language == 'es':
            return self.text_es or ''
        return self.text or ''

    def __str__(self):
        return self.title
