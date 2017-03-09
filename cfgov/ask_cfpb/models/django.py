from __future__ import absolute_import, unicode_literals

import HTMLParser

from django import forms
from django.apps import apps
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import html
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    FieldRowPanel)

from v1.util.migrations import get_or_create_page

html_parser = HTMLParser.HTMLParser()

PARENT_SLUG = 'ask-cfpb'


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
    featured_questions = models.ManyToManyField(
        'Answer', blank=True, related_name='featured_questions')
    panels = [
        FieldPanel('name', classname="title"),
        FieldPanel('slug'),
        FieldPanel('intro'),
        FieldPanel('name_es', classname="title"),
        FieldPanel('slug_es'),
        FieldPanel('intro_es'),
        FieldPanel('featured_questions'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Answer(models.Model):
    category = models.ManyToManyField('Category', blank=True)
    question = models.TextField(blank=True)
    snippet = RichTextField(blank=True, help_text="Optional answer intro")
    answer = RichTextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    question_es = models.TextField(blank=True)
    snippet_es = RichTextField(
        blank=True, help_text="Optional Spanish answer intro")
    answer_es = RichTextField(blank=True)
    slug_es = models.SlugField(max_length=255, blank=True)
    tagging = models.CharField(
        max_length=1000, blank=True, help_text="Tags used for search index")
    update_english_page = models.BooleanField(
        default=False,
        verbose_name="Update the English page when saving")
    update_spanish_page = models.BooleanField(
        default=False,
        verbose_name="Update the Spanish page when saving")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_edited = models.DateField(
        blank=True,
        null=True,
        help_text="Change the date to today "
                  "if you edit an English question, snippet or answer.")
    last_edited_es = models.DateField(
        blank=True,
        null=True,
        help_text="Change the date to today "
                  "if you edit a Spanish question, snippet or answer.")
    subcategory = models.ManyToManyField(
        'SubCategory',
        blank=True)
    audiences = models.ManyToManyField('Audience', blank=True)
    next_step = models.ForeignKey(
        NextStep,
        blank=True,
        null=True)
    related_questions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='related_question',
        help_text='Maximum of 3')

    def __str__(self):
        return "{} {}".format(self.id, self.slug)

    @property
    def available_subcategories(self):
        subcats = []
        for parent in self.category.all():
            subcats += list(parent.subcategory_set.all())
        return subcats

    panels = [
        MultiFieldPanel([
            FieldPanel('last_edited'),
            FieldPanel('last_edited_es'),
            FieldRowPanel([
                FieldPanel('update_english_page'),
                FieldPanel('update_spanish_page')])],
            heading="Workflow fields -- check before saving",
            classname="collapsible collapsed"),
        FieldPanel('question', classname="title"),
        FieldPanel('snippet', classname="full"),
        FieldPanel('answer', classname="full"),
        FieldPanel('slug'),
        FieldPanel('question_es', classname="title"),
        FieldPanel('snippet_es', classname="full"),
        FieldPanel('answer_es', classname="full"),
        FieldPanel('slug_es'),
        FieldPanel('audiences', widget=forms.CheckboxSelectMultiple),
        FieldPanel('next_step'),
        FieldPanel('category', widget=forms.CheckboxSelectMultiple),
        FieldPanel(
            'subcategory', widget=forms.CheckboxSelectMultiple),
        FieldPanel('related_questions', widget=forms.SelectMultiple),
        FieldPanel('tagging')
    ]

    def answer_text(self):
        """Unescapes and removes html tags from answer fields"""
        unescaped = ("{} {}".format(
            html_parser.unescape(self.snippet),
            html_parser.unescape(self.answer)))
        return html.strip_tags(unescaped).strip()

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

    def subcat_slugs(self):
        cats = [cat.slug for cat in self.subcategory.all()]
        return cats

    def category_text(self):
        if self.category.all():
            return [cat.name for cat in self.category.all()]
        else:
            return ''

    def audience_strings(self):
        for audience in self.audiences.all():
            yield audience.name

    def tags(self):
        for tag in self.tagging.split(','):
            tag = tag.replace('"', '')
            tag = tag.strip()
            if tag != u'':
                yield tag

    def create_or_update_page(self, language=None):
        """Create or update an English or Spanish Answer page"""
        answer_parent = Page.objects.get(slug=PARENT_SLUG)
        if language == 'en':
            _slug = self.slug
            _question = self.question
            _snippet = self.snippet
            _answer = self.answer
        elif language == 'es':
            _slug = self.slug_es
            _question = self.question_es
            _snippet = self.snippet_es
            _answer = self.answer_es
        else:
            raise ValueError('unsupported language: "{}"'.format(language))
        base_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerPage',
            '{}-{}-{}'.format(_question[:244], language, self.id),
            _slug,
            answer_parent,
            language=language,
            answer_base=self)
        page_update = base_page.get_latest_revision_as_page()
        page_update.question = _question
        page_update.answer = _answer
        page_update.snippet = _snippet
        page_update.has_unpublished_changes = True
        page_update.shared = False
        page_update.save_revision()
        return page_update

    def create_or_update_pages(self):
        counter = 0
        if self.answer:
            counter += 1
            self.create_or_update_page(language='en')
        if self.answer_es:
            counter += 1
            self.create_or_update_page(language='es')
        return counter

    def save(self, *args, **kwargs):
        if self.answer:
            self.slug = "{}-{}-{}".format(
                slugify(self.question[:244]), 'en', self.id)
        if self.answer_es:
            self.slug_es = "{}-{}-{}".format(
                slugify(self.question_es[:244]), 'es', self.id)
        if self.update_english_page:
            self.create_or_update_page(language='en')
        if self.update_spanish_page:
            self.create_or_update_page(language='es')
        super(Answer, self).save(*args, **kwargs)

    def delete(self):
        self.answer_pages.all().delete()
        super(Answer, self).delete()


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField()
    slug_es = models.SlugField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    weight = models.IntegerField(default=1)
    description = RichTextField(blank=True)
    description_es = RichTextField(blank=True)
    more_info = models.TextField(blank=True)
    parent = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        default=None)
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
        ordering = ['-weight']
        verbose_name_plural = "Subcategories"

# Search implementation to come

    # def get_absolute_url(self):
    #     return reverse('kbsearch') + \
    #         "?selected_facets=category_exact:" + self.slug

    # def get_babel_absolute_url(self):
    #     return reverse('babel_search') + \
    #         "?selected_facets=category_exact:" + self.slug_es

    # def search_query(self):
    #     from haystack.query import SearchQuerySet
    #     sqs = SearchQuerySet()
    #     sqs = sqs.models(Answer)
    #     sqs = sqs.filter(category=self.name)
    #     return sqs

    # def top_tags(self):
    #     sqs = self.search_query()
    #     sqs = sqs.facet('tag')
    #     return [pair[0] for pair
    #             in sqs.facet_counts()['fields']['tag']
    #             if pair[1] > 0]
