# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
import HTMLParser
import json

from django import forms
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import html
from django.utils.functional import cached_property
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    FieldRowPanel)
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page

from v1.util.migrations import get_or_create_page

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
    slug = models.SlugField()
    slug_es = models.SlugField()
    intro = RichTextField(blank=True)
    intro_es = RichTextField(blank=True)
    panels = [
        FieldPanel('name', classname="title"),
        FieldPanel('slug'),
        FieldPanel('intro'),
        FieldPanel('name_es', classname="title"),
        FieldPanel('slug_es'),
        FieldPanel('intro_es'),
    ]

    def __str__(self):
        return self.name

    def featured_answers(self):
        return Answer.objects.filter(
            category=self,
            featured=True).order_by('featured_rank')

    @cached_property
    def facet_map(self):
        answers = self.answer_set.order_by('-pk').select_related()
        subcats = self.subcategories.all().select_related()
        audiences = Audience.objects.all()
        container = {
            'subcategories': {},
            'audiences': {}
        }
        container['answers'] = OrderedDict([
            (str(answer.pk),
             {'question': answer.question,
              'url': '/ask-cfpb/slug-en-{}'.format(answer.pk)}
             ) for answer in answers if answer.english_page])
        subcat_data = {}
        for subcat in subcats:
            key = str(subcat.id)
            subcat_data[key] = [
                str(answer.pk) for answer
                in subcat.answer_set.all()
                if answer.english_page]
        container['subcategories'].update(subcat_data)
        audience_map = {audience: {'all': [], 'name': audience.name}
                        for audience in audiences}
        for answer in answers:
            for audience in audience_map:
                if audience in answer.audiences.all():
                    audience_map[audience]['all'].append(str(answer.pk))
        for subcat in subcats:
            ID = str(subcat.id)
            for audience in audience_map:
                _map = audience_map[audience]
                if _map['all']:
                    _map[ID] = []
                    for answer_id in subcat_data[ID]:
                        if answer_id in _map['all']:
                            _map[ID].append(answer_id)
        container['audiences'].update(
            {str(audience.id): audience_map[audience]
             for audience in audience_map.keys()})
        return container

    @cached_property
    def facet_json(self):
        return json.dumps(self.facet_map)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Answer(models.Model):
    last_user = models.ForeignKey(User, blank=True, null=True)
    category = models.ManyToManyField(
        'Category',
        blank=True,
        help_text="This associates an answer with a portal page")
    question = models.TextField(blank=True)
    statement = models.TextField(
        blank=True,
        help_text="Text to be used on portal pages to refer to this answer")
    snippet = RichTextField(blank=True, help_text="Optional answer intro")
    answer = RichTextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    featured = models.BooleanField(
        default=False,
        help_text="Makes the answer available to cards on the landing page")
    featured_rank = models.IntegerField(blank=True, null=True)

    question_es = models.TextField(
        blank=True,
        verbose_name="Spanish question")
    snippet_es = RichTextField(
        blank=True,
        help_text="Optional Spanish answer intro",
        verbose_name="Spanish snippet")
    answer_es = RichTextField(
        blank=True,
        verbose_name="Spanish answer")
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
        verbose_name="Send to English page for review")
    update_spanish_page = models.BooleanField(
        default=False,
        verbose_name="Send to Spanish page for review")
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
        help_text="Choose any subcategories related to the answer")
    audiences = models.ManyToManyField(
        'Audience',
        blank=True,
        help_text="Pick any audiences that may be interested in the answer")
    next_step = models.ForeignKey(
        NextStep,
        blank=True,
        null=True,
        help_text="Also called action items or upsell items")
    related_questions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='related_question',
        help_text='Maximum of 3')

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('update_english_page'),
                FieldPanel('last_edited')]),
            FieldRowPanel([
                FieldPanel('update_spanish_page'),
                FieldPanel('last_edited_es')])],
            heading="Workflow fields -- check before saving",
            classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('question', classname="title"),
            FieldPanel('statement', classname="title"),
            FieldPanel('snippet', classname="full"),
            FieldPanel('answer', classname="full")],
            heading="English",
            classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('question_es', classname="title"),
            FieldPanel('snippet_es', classname="full"),
            FieldPanel('answer_es', classname="full")],
            heading="Spanish",
            classname="collapsible"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('featured'),
                FieldPanel('featured_rank')]),
            FieldPanel('audiences', widget=forms.CheckboxSelectMultiple),
            FieldPanel('next_step'),
            FieldRowPanel([
                FieldPanel(
                    'category', widget=forms.CheckboxSelectMultiple),
                FieldPanel(
                    'subcategory',
                    widget=forms.CheckboxSelectMultiple)]),
            FieldPanel('related_questions', widget=forms.SelectMultiple),
            FieldPanel('search_tags')],
            heading="Metadata",
            classname="collapsible"),
    ]

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

    @property
    def available_subcategory_qs(self):
        return SubCategory.objects.filter(parent__in=self.category.all())

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

    @staticmethod
    def clean_tag_list(taglist):
        return [
            tag.replace('"', '').strip()
            for tag in taglist.split(',')
            if tag.replace('"', '').strip()]

    @cached_property
    def tags(self):
        return self.clean_tag_list(self.search_tags)

    @cached_property
    def tags_es(self):
        return self.clean_tag_list(self.search_tags_es)

    @classmethod
    def valid_spanish_tags(cls):
        """
        Search tags are arbitrary and messy. This function serves 2 purposes:
        - Assemble a whitelist of tags that are safe for search.
        - Exclude tags that are attached to only one answer.
        Tags are useless until they can be used to collect at least 2 answers.
        """
        cleaned = []
        valid = []
        for a in cls.objects.all():
            if a.search_tags_es.strip():
                cleaned += [
                    tag.strip() for tag
                    in a.search_tags_es.strip().split(',')
                    if tag.strip()]
        for tag in sorted(set(cleaned)):
            if cls.objects.filter(search_tags_es__contains=tag).count() > 1:
                valid.append(tag)
        return valid

    def has_live_page(self):
        if not self.answer_pages.all():
            return False
        for page in self.answer_pages.all():
            if page.live:
                return True
        return False

    def create_or_update_page(self, language=None):
        """Create or update an English or Spanish Answer page"""
        from .pages import AnswerPage
        english_parent = Page.objects.get(slug=ENGLISH_PARENT_SLUG).specific
        spanish_parent = Page.objects.get(slug=SPANISH_PARENT_SLUG).specific
        if language == 'en':
            _parent = english_parent
            _slug = self.slug
            _question = self.question
            _snippet = self.snippet
            _answer = self.answer
        elif language == 'es':
            _parent = spanish_parent
            _slug = self.slug_es
            _question = self.question_es
            _snippet = self.snippet_es
            _answer = self.answer_es
        else:
            raise ValueError('unsupported language: "{}"'.format(language))
        try:
            base_page = AnswerPage.objects.get(
                language=language, answer_base=self)
        except ObjectDoesNotExist:
            base_page = get_or_create_page(
                apps,
                'ask_cfpb',
                'AnswerPage',
                '{}-{}-{}'.format(_question[:244], language, self.id),
                _slug,
                _parent,
                show_in_menus=True,
                language=language,
                answer_base=self)
            base_page.save_revision(user=self.last_user)
        _page = base_page.get_latest_revision_as_page()
        _page.question = _question
        _page.answer = _answer
        _page.snippet = _snippet
        _page.title = '{}-{}-{}'.format(
            _question[:244], language, self.id)
        _page.live = False
        _page.has_unpublished_changes = True
        stream_block = _page.content.stream_block
        _page.content = StreamValue(
            stream_block,
            get_feedback_stream_value(_page),
            is_lazy=True)
        _page.save_revision(user=self.last_user)
        base_page.refresh_from_db()
        base_page.has_unpublished_changes = True
        base_page.save()
        return base_page

    def create_or_update_pages(self):
        counter = 0
        if self.answer:
            counter += 1
            self.create_or_update_page(language='en')
        if self.answer_es:
            counter += 1
            self.create_or_update_page(language='es')
        return counter

    def save(self, skip_page_update=False, *args, **kwargs):
        if self.answer:
            self.slug = "{}-en-{}".format(
                slugify(self.question[:244]), self.id)
        else:
            self.slug = "slug-en-{}".format(self.id)
        if self.answer_es:
            self.slug_es = "{}-es-{}".format(
                slugify(self.question_es[:244]), self.id)
        super(Answer, self).save(*args, **kwargs)
        if skip_page_update is False:
            if self.update_english_page:
                self.create_or_update_page(language='en')
            if self.update_spanish_page:
                self.create_or_update_page(language='es')

    def delete(self):
        self.answer_pages.all().delete()
        super(Answer, self).delete()


class EnglishAnswerProxy(Answer):
    """A no-op proxy class to allow separate language indexing in Haystack"""
    class Meta:
        proxy = True


class SpanishAnswerProxy(Answer):
    """A no-op proxy class to allow separate language indexing in Haystack"""
    class Meta:
        proxy = True


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField()
    slug_es = models.SlugField(null=True, blank=True)
    weight = models.IntegerField(default=1)
    description = RichTextField(blank=True)
    description_es = RichTextField(blank=True)
    more_info = models.TextField(blank=True)
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
    )

    panels = [
        FieldPanel('name', classname="title"),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('name_es', classname="title"),
        FieldPanel('slug_es'),
        FieldPanel('description_es'),
        FieldPanel('featured'),
        FieldPanel('weight'),
        FieldPanel('more_info'),
        FieldPanel('parent'),
        FieldPanel('related_subcategories',
                   widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['weight']
        verbose_name_plural = "Subcategories"
