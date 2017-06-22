from __future__ import absolute_import, unicode_literals

import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from haystack.query import SearchQuerySet


from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface)
from wagtail.contrib.wagtailroutablepage.models import (
    RoutablePageMixin, route)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField

from v1 import blocks as v1_blocks
from v1.models import CFGOVPage, CFGOVPageManager, LandingPage
from v1.models.snippets import ReusableText


SPANISH_ANSWER_SLUG_BASE = '/es/obtener-respuestas/slug-es-{}/'
ENGLISH_ANSWER_SLUG_BASE = '/ask-cfpb/slug-en-{}/'
ABOUT_US_SNIPPET_TITLE = 'About us (For consumers)'
ENGLISH_DISCLAIMER_SNIPPET_TITLE = 'Legal disclaimer for consumer materials'
SPANISH_DISCLAIMER_SNIPPET_TITLE = (
    'Legal disclaimer for consumer materials (in Spanish)')


# def get_valid_spanish_tags():
#     from ask_cfpb.models import Answer, AnswerTagProxy
#     try:
#         sqs = SearchQuerySet().models(AnswerTagProxy)
#         valid_spanish_tags = sqs.filter(content='tags')[0].valid_spanish
#     except (IndexError, AttributeError):  # ES not available; go to plan B
#         valid_spanish_tags = Answer.valid_spanish_tags()['valid_tags']
#     return valid_spanish_tags


def get_reusable_text_snippet(snippet_title):
    try:
        return ReusableText.objects.get(
            title=snippet_title)
    except ReusableText.DoesNotExist:
        pass


def get_ask_nav_items(request, current_page):
    from ask_cfpb.models import Category
    return [
        {
            'title': cat.name,
            'url': '/ask-cfpb/category-' + cat.slug,
            'active': False if not hasattr(current_page, 'ask_category')
            else cat.name == current_page.ask_category.name,
            'expanded': True
        }
        for cat in Category.objects.all()
    ], True


def get_ask_breadcrumbs(category=None):
    breadcrumbs = [{'title': 'Ask CFPB', 'href': '/ask-cfpb/'}]
    if category:
        breadcrumbs.append({
            'title': category.name,
            'href': '/ask-cfpb/category-{}'.format(category.slug)
        })
    return breadcrumbs


class AnswerLandingPage(LandingPage):
    """
    Page type for Ask CFPB's landing page.
    """
    content_panels = [
        StreamFieldPanel('header')
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(LandingPage.settings_panels, heading='Configuration'),
    ])
    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        from ask_cfpb.models import Category, Audience
        context = super(AnswerLandingPage, self).get_context(request)
        context['categories'] = Category.objects.all()
        if self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['audiences'] = [
                {'text': audience.name,
                 'url': '/ask-cfpb/audience-{}'.format(
                        slugify(audience.name))}
                for audience in Audience.objects.all().order_by('name')]
        return context

    def get_template(self, request):
        if self.language == 'es':
            return 'ask-cfpb/landing-page-spanish.html'

        return 'ask-cfpb/landing-page.html'


class AnswerCategoryPage(RoutablePageMixin, CFGOVPage):
    """
    A routable page type for Ask CFPB category pages and their subcategories.
    """
    from ask_cfpb.models import Answer, Audience, Category, SubCategory

    objects = CFGOVPageManager()
    content = StreamField([], null=True)
    ask_category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='category_page')
    ask_subcategory = models.ForeignKey(
        SubCategory,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='subcategory_page')
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('ask_category', Category),
        StreamFieldPanel('content'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def get_template(self, request):
        if self.language == 'es':
            return 'ask-cfpb/category-page-spanish.html'

        return 'ask-cfpb/category-page.html'

    def add_page_js(self, js):
        if self.language == 'en':
            super(AnswerCategoryPage, self).add_page_js(js)
            js['template'] += ['secondary-navigation.js']

    def get_context(self, request, *args, **kwargs):
        context = super(
            AnswerCategoryPage, self).get_context(request, *args, **kwargs)
        sqs = SearchQuerySet().models(self.Category)
        if self.language == 'es':
            sqs = sqs.filter(content=self.ask_category.name_es)
        else:
            sqs = sqs.filter(content=self.ask_category.name)
        if sqs:
            facet_map = sqs[0].facet_map
        else:
            facet_map = self.ask_category.facet_map
        facet_dict = json.loads(facet_map)
        subcat_ids = facet_dict['subcategories'].keys()
        answer_ids = facet_dict['answers'].keys()
        audience_ids = facet_dict['audiences'].keys()
        subcats = self.SubCategory.objects.filter(
            pk__in=subcat_ids).values(
                'id', 'slug', 'slug_es', 'name', 'name_es')
        answers = self.Answer.objects.filter(
            pk__in=answer_ids).order_by('-pk').values(
                'id', 'question', 'question_es',
                'slug', 'slug_es', 'answer_es')
        for a in answers:
            a['answer_es'] = Truncator(a['answer_es']).words(
                40, truncate=' ...')
        audiences = self.Audience.objects.filter(
            pk__in=audience_ids).values('id', 'name')
        context.update({
            'answers': answers,
            'audiences': audiences,
            'facet_map': facet_map,
            'choices': subcats,
            'results_count': answers.count(),
            'get_secondary_nav_items': get_ask_nav_items
        })

        if self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['breadcrumb_items'] = get_ask_breadcrumbs()
        elif self.language == 'es':
            context['tags'] = self.ask_category.top_tags_es
        return context

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.ask_category.category_image

    @route(r'^$')
    def category_page(self, request):
        try:
            context = self.get_context(request)
            page = int(request.GET.get('page', 1))
            paginator = Paginator(context.get('answers'), 20)
            context.update({
                'paginator': paginator,
                'current_page': int(page),
                'questions': paginator.page(page),
            })
        except (EmptyPage, PageNotAnInteger):
            request.GET = request.GET.copy()
            request.GET['page'] = 1
            context = self.get_context(request)
            page = int(request.GET.get('page', 1))
            paginator = Paginator(context.get('answers'), 20)
            context.update({
                'paginator': paginator,
                'current_page': int(page),
                'questions': paginator.page(page),
            })

        return TemplateResponse(
            request,
            self.get_template(request),
            context)

    @route(r'^(?P<subcat>[^/]+)/$')
    def subcategory_page(self, request, **kwargs):
        subcat = self.SubCategory.objects.filter(
            slug=kwargs.get('subcat')).first()
        if subcat:
            self.ask_subcategory = subcat
        else:
            raise Http404
        answers = self.ask_subcategory.answer_set.order_by(
            '-pk').values(
            'id', 'question', 'slug')
        try:
            context = self.get_context(request)
            page = request.GET.get('page', 1)
            paginator = Paginator(answers, 20)
            context.update({
                'paginator': paginator,
                'current_page': int(page),
                'results_count': answers.count(),
                'questions': paginator.page(page),
                'breadcrumb_items': get_ask_breadcrumbs(
                    self.ask_category)
            })
        except (EmptyPage, PageNotAnInteger):
            request.GET = request.GET.copy()
            request.GET['page'] = 1
            context = self.get_context(request)
            page = request.GET.get('page', 1)
            paginator = Paginator(answers, 20)
            context.update({
                'paginator': paginator,
                'current_page': int(page),
                'results_count': answers.count(),
                'questions': paginator.page(page),
                'breadcrumb_items': get_ask_breadcrumbs(
                    self.ask_category)
            })

        return TemplateResponse(
            request,
            self.get_template(request),
            context)


class AnswerResultsPage(CFGOVPage):

    objects = CFGOVPageManager()
    answers = []

    content = StreamField([
    ], null=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('content'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def add_page_js(self, js):
        if self.language == 'en':
            super(AnswerResultsPage, self).add_page_js(js)
            js['template'] += ['secondary-navigation.js']

    def get_context(self, request, **kwargs):

        context = super(
            AnswerResultsPage, self).get_context(request, **kwargs)
        page = int(request.GET.get('page', 1))
        context.update(**kwargs)
        paginator = Paginator(self.answers, 20)
        if page > paginator.num_pages:
            page = 1
        context['current_page'] = page
        context['paginator'] = paginator
        context['results'] = paginator.page(page)
        context['results_count'] = len(self.answers)
        context['get_secondary_nav_items'] = get_ask_nav_items

        if self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['breadcrumb_items'] = get_ask_breadcrumbs()

        return context

    def get_template(self, request):
        if self.language == 'en':
            return 'ask-cfpb/answer-search-results.html'
        elif self.language == 'es':
            return 'ask-cfpb/answer-search-spanish-results.html'


class AnswerAudiencePage(CFGOVPage):
    from ask_cfpb.models import Audience

    objects = CFGOVPageManager()
    content = StreamField([
    ], null=True)
    ask_audience = models.ForeignKey(
        Audience,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='audience_page')
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('ask_audience', Audience),
        StreamFieldPanel('content'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def add_page_js(self, js):
        if self.language == 'en':
            super(AnswerAudiencePage, self).add_page_js(js)
            js['template'] += ['secondary-navigation.js']

    def get_context(self, request, *args, **kwargs):
        from ask_cfpb.models import Answer
        context = super(AnswerAudiencePage, self).get_context(request)
        answers = Answer.objects.filter(audiences__id=self.ask_audience.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(answers, 20)
        if page > paginator.num_pages:
            page = 1
        context.update({
            'answers': paginator.page(page),
            'current_page': int(page),
            'paginator': paginator,
            'results_count': len(answers),
            'get_secondary_nav_items': get_ask_nav_items
        })

        if self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['breadcrumb_items'] = get_ask_breadcrumbs()

        return context

    template = 'ask-cfpb/audience-page.html'


class TagResultsPage(RoutablePageMixin, AnswerResultsPage):
    """A routable page for serving Answers by tag"""

    objects = CFGOVPageManager()
    language = 'es'

    def get_template(self, request):
        """We only offer tag search on Spanish pages"""
        return 'ask-cfpb/answer-tag-spanish-results.html'

    @route(r'^$')
    def spanish_tag_base(self, request):
        raise Http404

    @route(r'^(?P<tag>[^/]+)/$')
    def buscar_por_etiqueta(self, request, **kwargs):
        from ask_cfpb.models import Answer
        tag_dict = Answer.valid_spanish_tags()
        tag = kwargs.get('tag').replace('_', ' ')
        if not tag or tag not in tag_dict['valid_tags']:
            raise Http404
        self.answers = [
            (SPANISH_ANSWER_SLUG_BASE.format(a.id),
             a.question_es,
             Truncator(a.answer_es).words(40, truncate=' ...'))
            for a in tag_dict['tag_map'][tag]
        ]
        try:
            context = self.get_context(request)
            page = int(request.GET.get('page', 1))
            paginator = Paginator(self.answers, 20)
            context['results'] = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            request.GET = request.GET.copy()
            request.GET['page'] = 1
            context = self.get_context(request)
            page = int(request.GET.get('page', 1))
            paginator = Paginator(self.answers, 20)
            context['results'] = paginator.page(page)
        context['results_count'] = len(self.answers)
        context['tag'] = tag
        context['paginator'] = paginator
        context['current_page'] = page
        return TemplateResponse(
            request,
            self.get_template(request),
            context)


class AnswerPage(CFGOVPage):
    """
    Page type for Ask CFPB answers.
    """
    from ask_cfpb.models import Answer
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

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerPage, self).get_context(request)
        context['answer_id'] = self.answer_base.id
        context['related_questions'] = self.answer_base.related_questions.all()
        context['category'] = self.answer_base.category.first()
        context['description'] = self.snippet if self.snippet \
            else Truncator(self.answer).words(40, truncate=' ...')
        subcategories = []
        for subcat in self.answer_base.subcategory.all():
            subcategories.append(subcat)
            for related in subcat.related_subcategories.all():
                subcategories.append(related)
        context['subcategories'] = set(subcategories)
        context['audiences'] = [
            {'text': audience.name,
             'url': '/ask-cfpb/audience-{}'.format(
                    slugify(audience.name))}
            for audience in self.answer_base.audiences.all()]
        if self.language == 'es':
            tag_dict = self.Answer.valid_spanish_tags()
            context['tags_es'] = [tag for tag in self.answer_base.tags_es
                                  if tag in tag_dict['valid_tags']]
            context['tweet_text'] = Truncator(self.question).chars(
                100, truncate=' ...')
            context['disclaimer'] = get_reusable_text_snippet(
                SPANISH_DISCLAIMER_SNIPPET_TITLE)
        elif self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['last_edited'] = self.answer_base.last_edited
            context['breadcrumb_items'] = get_ask_breadcrumbs(
                self.answer_base.category.first())

        return context

    def get_template(self, request):
        printable = request.GET.get('print', False)
        if self.language == 'es':
            if printable == 'true':
                return 'ask-cfpb/answer-page-spanish-printable.html'

            return 'ask-cfpb/answer-page-spanish.html'

        return 'ask-cfpb/answer-page.html'

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

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        if self.answer_base.social_sharing_image:
            return self.answer_base.social_sharing_image

        if not self.answer_base.category.exists():
            return None

        return self.answer_base.category.first().category_image
