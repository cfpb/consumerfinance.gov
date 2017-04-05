from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface)
# from wagtail.wagtailcore.blocks import StreamBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField
# from modelcluster.fields import ParentalKey
# from wagtail.wagtailcore.models import Orderable

from v1 import blocks as v1_blocks
from v1.models import CFGOVPage
# from ask_cfpb.models import Answer


# class FeedbackBlock(StreamBlock):
#     feedback_block = v1_blocks.Feedback()

#     class Meta:
#         default = None


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

    feedback_block = StreamField([
        ('feedback', v1_blocks.Feedback())
    ], default=None)

    content_panels = CFGOVPage.content_panels + [
        FieldPanel('redirect_to'),
    ]

    settings_panels = CFGOVPage.settings_panels + [
        StreamFieldPanel('feedback_block'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('question'),
        index.SearchField('answer'),
        index.SearchField('answer_base'),
        index.FilterField('language')
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    template = 'ask-answer-page/index.html'
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
