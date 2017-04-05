from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    ObjectList,
    TabbedInterface)

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtailsearch import index
from v1.forms import FeedbackForm
from v1.models import CFGOVPage
from v1.blocks import Feedback 

# from ask_cfpb.models import Answer

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
        on_delete=models.PROTECT)


    content_panels = CFGOVPage.content_panels + [
        FieldPanel('answer_base', Answer),
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

    objects = PageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerPage, self).get_context(request)
        context['related_questions'] = self.answer_base.related_questions.all()
        context['category'] = self.answer_base.category.all()[0]
        context['subcategories'] = self.answer_base.subcategory.all()
        #context['feedback'] = FeedbackForm()
        #context['form_modules'] = {'content': {0: {'form': context['feedback']}}}
        return context

    def get_template(self, request):
        print request
        if self.language == 'es':
            return 'ask-answer-page/spanish.html'

        return 'ask-answer-page/index.html'

    def __str__(self):
        if self.answer_base:
            return '{}: {}'.format(self.answer_base.id, self.title)
        else:
            return self.title
