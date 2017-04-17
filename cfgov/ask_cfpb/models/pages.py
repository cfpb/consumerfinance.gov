from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface)
# from wagtail.wagtailcore.blocks import CharBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField

from v1 import blocks as v1_blocks
from v1.atomic_elements.organisms import FilterControls
from v1.feeds import FilterableFeedPageMixin
from v1.models import CFGOVPage, LandingPage
from v1.util.filterable_list import FilterableListMixin


class AnswerLandingPage(LandingPage):
    """
    Page type for Ask CFPB's landing page.
    """
    content_panels = [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(LandingPage.settings_panels, heading='Configuration'),
    ])
    objects = PageManager()
    template = 'ask-cfpb/landing-page.html'


class AnswerCategoryPage(
        FilterableFeedPageMixin, FilterableListMixin, CFGOVPage):
    """
    Page type for Ask CFPB parent-category pages.
    """
    from .django import Category

    objects = PageManager()
    content = StreamField([
        ('filter_controls', FilterControls()),
    ], null=True)
    ask_category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='category_page')
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('ask_category', Category),
        StreamFieldPanel('content'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])
    template = 'ask-cfpb/category-page.html'

    def add_page_js(self, js):
        super(AnswerCategoryPage, self).add_page_js(js)
        js['template'] += ['secondary-navigation.js']

    def get_context(self, request, *args, **kwargs):
        context = super(
            AnswerCategoryPage, self).get_context(request, *args, **kwargs)
        context.update({
            'choices':
            self.ask_category.subcategories.all().values_list(
                'slug', 'name')
        })
        return context


class AnswerPage(CFGOVPage):
    """
    Page type for Ask CFPB answers.
    """
    from .django import Answer
    question = RichTextField(blank=True, editable=False)
    answer = RichTextField(blank=True, editable=False)
    snippet = RichTextField(
        blank=True, help_text='Optional answer intro', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=timezone.now)
    answer_base = models.ForeignKey(
        Answer,
        blank=True,
        null=True,
        related_name='answer_pages',
        on_delete=models.SET_NULL)
    redirect_to = models.ForeignKey(
        Answer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='redirected_pages',
        help_text="Choose another Answer to redirect this page to")

    content = StreamField([
        ('feedback', v1_blocks.Feedback()),
    ], blank=True)

    content_panels = CFGOVPage.content_panels + [
        FieldPanel('redirect_to'),
        StreamFieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('question'),
        index.SearchField('answer'),
        index.SearchField('answer_base'),
        index.FilterField('language')
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'ask-cfpb/answer-page.html'
    objects = PageManager()

    def __str__(self):
        if self.answer_base:
            return '{}: {}'.format(self.answer_base.id, self.title)
        else:
            return self.title

    @property
    def status_string(self):
        if self.redirect_to:
            if not self.live:
                return _("redirected but not live")
            else:
                return _("redirected")
        else:
            return super(AnswerPage, self).status_string
