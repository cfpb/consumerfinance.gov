# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import Counter
from six.moves import html_parser as HTMLParser

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import html

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


html_parser = HTMLParser.HTMLParser()

ENGLISH_PARENT_SLUG = 'ask-cfpb'
SPANISH_PARENT_SLUG = 'obtener-respuestas'


def get_feedback_stream_value(page):
    """Delivers a basic feedback module with yes/no buttons and comment box"""
    translation_text = {
        'helpful': {'es': '¿Fue útil esta respuesta?',
                    'en': 'Was this page helpful to you?'},
        'button': {'es': 'Enviar',
                   'en': 'Submit'}
    }
    stream_value = [
        {'type': 'feedback',
         'value': {
             'was_it_helpful_text': translation_text['helpful'][page.language],
             'button_text': translation_text['button'][page.language],
             'intro_text': '',
             'question_text': '',
             'radio_intro': '',
             'radio_text': ('This information helps us '
                            'understand your question better.'),
             'radio_question_1': 'How soon do you expect to buy a home?',
             'radio_question_2': 'Do you currently own a home?',
             'contact_advisory': ''}}]
    return stream_value


def generate_short_slug(slug_string):
    """Limits a slug to around 100 characters, using full words"""
    if len(slug_string) < 100:
        return slugify(slug_string)
    slug_100 = slugify(slug_string)[:100]
    if slug_100.endswith('-'):
        slug_base = slug_100.rstrip('-')
    else:
        slug_base = "-".join(slug_100.split('-')[:-1])
    return slug_base


class Audience(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


class NextStep(models.Model):
    title = models.CharField(max_length=255)
    show_title = models.BooleanField(default=False)
    text = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('show_title'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255)
    slug = models.SlugField(help_text="Do not edit this field")
    slug_es = models.SlugField(help_text="Do not edit this field")
    intro = RichTextField(
        blank=True,
        help_text=(
            "Do not use H2, H3, H4, or H5 to style this text. "
            "Do not add links, images, videos or other rich text elements."))
    intro_es = RichTextField(
        blank=True,
        help_text=(
            "Do not use this field. "
            "It is not currently displayed on the front end."))
    category_image = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            'Select a custom image to appear when visitors share pages '
            'belonging to this category on social media.'
        )
    )
    panels = [
        FieldPanel('name', classname="title"),
        FieldPanel('slug'),
        FieldPanel('intro'),
        FieldPanel('name_es', classname="title"),
        FieldPanel('slug_es'),
        FieldPanel('intro_es'),
        ImageChooserPanel('category_image')
    ]

    def __str__(self):
        return self.name

    def featured_answers(self, language):
        return self.answerpage_set.filter(
            language=language,
            category=self,
            featured=True).order_by('featured_rank')

    @property
    def top_tags(self, language='es'):
        search_tags = []
        pages = self.answerpage_set.filter(language=language).all()
        for page in pages:
            search_tags += page.clean_search_tags
        counter = Counter(search_tags)
        return counter.most_common()[:10]

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField()
    slug_es = models.SlugField(
        null=True,
        blank=True,
        help_text="This field is not currently used on the front end.")
    weight = models.IntegerField(default=1)
    description = RichTextField(
        blank=True,
        help_text="This field is not currently displayed on the front end.")
    description_es = RichTextField(
        blank=True,
        help_text="This field is not currently displayed on the front end.")
    more_info = models.TextField(
        blank=True,
        help_text="This field is not currently displayed on the front end.")
    parent = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        default=None,
        related_name='subcategories')
    related_subcategories = models.ManyToManyField(
        'self',
        blank=True,
        default=None,
        help_text="Maximum 3 related subcategories"
    )

    panels = [
        FieldPanel('name', classname="title"),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('name_es', classname="title"),
        FieldPanel('slug_es'),
        FieldPanel('description_es'),
        FieldPanel('weight'),
        FieldPanel('more_info'),
        FieldPanel('parent'),
        FieldPanel('related_subcategories',
                   widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return "{}: {}".format(self.parent.name, self.name)

    class Meta:
        ordering = ['weight']
        verbose_name_plural = "subcategories"


class Answer(models.Model):
    last_user = models.ForeignKey(User, blank=True, null=True)
    category = models.ManyToManyField(
        'Category',
        blank=True,
        help_text=(
            "Categorize this answer. "
            "Avoid putting into more than one category."))
    question = models.TextField(blank=True)
    statement = models.TextField(
        blank=True,
        help_text=(
            "(Optional) Use this field to rephrase the question title as "
            "a statement. Use only if this answer has been chosen to appear "
            "on a money topic portal (e.g. /consumer-tools/debt-collection)."))
    snippet = RichTextField(
        blank=True,
        help_text=(
            "Optional answer intro, 180-200 characters max. "
            "Avoid adding links, images, videos or other rich text elements."))
    answer = RichTextField(
        blank=True,
        help_text=(
            "Do not use H2 or H3 to style text. Only use the HTML Editor "
            "for troubleshooting. To style tips, warnings and notes, "
            "select the content that will go inside the rule lines "
            "(so, title + paragraph) and click the Pencil button "
            "to style it. Click again to unstyle the tip."))
    slug = models.SlugField(max_length=255, blank=True)
    featured = models.BooleanField(
        default=False,
        help_text=(
            "Check to make this one of two featured answers "
            "on the landing page."))
    featured_rank = models.IntegerField(blank=True, null=True)

    question_es = models.TextField(
        blank=True,
        verbose_name="Spanish question")
    snippet_es = RichTextField(
        blank=True,
        help_text=(
            "Do not use this field. "
            "It is not currently displayed on the front end."),
        verbose_name="Spanish snippet")
    answer_es = RichTextField(
        blank=True,
        verbose_name="Spanish answer",
        help_text=(
            "Do not use H2 or H3 to style text. Only use the HTML Editor "
            "for troubleshooting. Also note that tips styling "
            "(the Pencil button) does not display on the front end."))
    slug_es = models.SlugField(
        max_length=255,
        blank=True,
        verbose_name="Spanish slug")
    search_tags = models.CharField(
        max_length=1000,
        blank=True,
        help_text="Search words or phrases, separated by commas")
    search_tags_es = models.CharField(
        max_length=1000,
        blank=True,
        help_text="Spanish search words or phrases, separated by commas")
    update_english_page = models.BooleanField(
        default=False,
        verbose_name="Send to English page for review",
        help_text=(
            "Check this box to push your English edits "
            "to the page for review. This does not publish your edits."))
    update_spanish_page = models.BooleanField(
        default=False,
        verbose_name="Send to Spanish page for review",
        help_text=(
            "Check this box to push your Spanish edits "
            "to the page for review. This does not publish your edits."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_edited = models.DateField(
        blank=True,
        null=True,
        help_text="Change the date to today "
                  "if you edit an English question, snippet or answer.",
        verbose_name="Last edited English content")
    last_edited_es = models.DateField(
        blank=True,
        null=True,
        help_text="Change the date to today "
                  "if you edit a Spanish question, snippet or answer.",
        verbose_name="Last edited Spanish content")
    subcategory = models.ManyToManyField(
        'SubCategory',
        blank=True,
        help_text=(
            "Choose only subcategories that belong "
            "to one of the categories checked above."))
    audiences = models.ManyToManyField(
        'Audience',
        blank=True,
        help_text="Tag any audiences that may be interested in the answer.")
    next_step = models.ForeignKey(
        NextStep,
        blank=True,
        null=True,
        help_text=(
            "Formerly known as action items or upsell items."
            "On the web page, these are labeled as "
            "'Explore related resources.'"))
    related_questions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='related_question',
        help_text='Maximum of 3')
    social_sharing_image = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            'Optionally select a custom image to appear when users share this '
            'page on social media websites. If no image is selected, this '
            'page\'s category image will be used. '
            'Recommended size: 1200w x 630h. '
            'Maximum size: 4096w x 4096h.'
        )
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{} {}".format(self.id, self.slug)

    @property
    def english_page(self):
        return self.answer_pages.filter(language='en').first()

    @property
    def spanish_page(self):
        return self.answer_pages.filter(language='es').first()

    @property
    def answer_text(self):
        """Unescapes and removes html tags from answer fields"""
        unescaped = ("{} {}".format(
            html_parser.unescape(self.snippet),
            html_parser.unescape(self.answer)))
        return html.strip_tags(unescaped).strip()

    @property
    def answer_text_es(self):
        """Unescapes and removes html tags from Spanish answer fields"""
        unescaped = ("{} {}".format(
            html_parser.unescape(self.snippet_es),
            html_parser.unescape(self.answer_es)))
        return html.strip_tags(unescaped).strip()

    def cleaned_questions(self):
        cleaned_terms = html_parser.unescape(self.question)
        return [html.strip_tags(cleaned_terms).strip()]

    def cleaned_questions_es(self):
        cleaned_terms = html_parser.unescape(self.question_es)
        return [html.strip_tags(cleaned_terms).strip()]

    def category_text(self):
        if self.category.all():
            return [cat.name for cat in self.category.all()]
        else:
            return ''

    def category_text_es(self):
        if self.category.all():
            return [cat.name_es for cat in self.category.all()]
        else:
            return ''

    def audience_strings(self):
        return [audience.name for audience in self.audiences.all()]
