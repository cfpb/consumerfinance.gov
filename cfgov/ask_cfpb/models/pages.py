from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    ObjectList,
    TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtailsearch import index

from v1.models import CFGOVPage
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
    redirect_id = models.IntegerField(
        blank=True,
        null=True,
        help_text="Enter an Answer ID to redirect this page to")

    content_panels = CFGOVPage.content_panels + [
        FieldPanel('answer_base', Answer),
        FieldPanel('redirect_id')
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

    template = 'ask-answer-page/index.html'
    objects = PageManager()

    def __str__(self):
        if self.answer_base:
            return '{}: {}'.format(self.answer_base.id, self.title)
        else:
            return self.title

    @property
    def status_string(self):
        if self.redirect_id:
            if not self.live:
                return _("redirected but not live")
            else:
                return _("redirected")
        if not self.live:
            if self.expired:
                return _("expired")
            elif self.approved_schedule:
                return _("scheduled")
            else:
                return _("draft")
        else:
            if self.has_unpublished_changes:
                return _("live + draft")
            else:
                return _("live")
