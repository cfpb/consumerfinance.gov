from __future__ import absolute_import, unicode_literals

import json
import re
from six.moves.urllib.parse import urlparse

from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from haystack.query import SearchQuerySet

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage, CFGOVPageManager, LandingPage
from v1.models.snippets import ReusableText


SPANISH_ANSWER_SLUG_BASE = '/es/obtener-respuestas/slug-es-{}/'
ENGLISH_ANSWER_SLUG_BASE = '/ask-cfpb/slug-en-{}/'
ABOUT_US_SNIPPET_TITLE = 'About us (For consumers)'
ENGLISH_DISCLAIMER_SNIPPET_TITLE = 'Legal disclaimer for consumer materials'
SPANISH_DISCLAIMER_SNIPPET_TITLE = (
    'Legal disclaimer for consumer materials (in Spanish)')
CONSUMER_TOOLS_PORTAL_PAGES = {
    '/consumer-tools/auto-loans/': (
        'Auto Loans',
        'auto-loans'),
    '/consumer-tools/bank-accounts/': (
        'Bank Accounts and Services',
        'bank-accounts-and-services'),
    '/consumer-tools/credit-cards/': (
        'Credit Cards',
        'credit-cards'),
    '/consumer-tools/credit-reports-and-scores/': (
        'Credit Reports and Scores',
        'credit-reporting'),
    '/consumer-tools/debt-collection/': (
        'Debt Collection',
        'debt-collection'),
    '/consumer-tools/prepaid-cards/': (
        'Prepaid Cards',
        'prepaid-cards'),
    '/consumer-tools/sending-money/': (
        'Sending Money',
        'money-transfers'),
    '/consumer-tools/student-loans/': (
        'Student Loans',
        'student-loans')
}
JOURNEY_PATHS = (
    '/owning-a-home/prepare',
    '/owning-a-home/explore',
    '/owning-a-home/compare',
    '/owning-a-home/close',
    '/owning-a-home/process',
)


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
            'url': '/ask-cfpb/category-' + cat.slug + '/',
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


def get_journey_breadcrumbs(request, path):
    """
    If referrer is a BAH journey page, breadcrumbs should
    reflect the BAH journey page hierarchy.
    """
    pages = path.replace('process/', '').strip('/').split('/')
    # TODO: replace when journey page urls are updated
    # after 2018 homebuying season campaign ends
    # Also remove related tests
    if pages == ['owning-a-home']:
        pages.append('prepare')
    # end TODO
    breadcrumbs = []
    parent = request.site.root_page
    idx = 0
    while idx < len(pages):
        page = parent.get_children().get(slug=pages[idx])
        # TODO: replace when journey page urls are updated
        # after 2018 homebuying season campaign ends
        if len(breadcrumbs):
            href = page.relative_url(request.site).replace(
                '/owning-a-home/',
                '/owning-a-home/process/'
            )
        else:
            href = page.relative_url(request.site)
        # end TODO
        breadcrumbs.append({
            'title': page.title,
            'href': href
        })
        parent = page
        idx += 1
    return breadcrumbs


def get_question_referrer_data(request, categories):
    """
    Determines whether a question page's referrer is a
    portal, Ask category, or BAH journey page. If so, returns
    the appropriate category and breadcrumbs. Otherwise, returns
    question's first category and its breadcrumbs.
    """
    try:
        referrer = request.META.get('HTTP_REFERER', '')
        path = urlparse(referrer).path
        portal_data = CONSUMER_TOOLS_PORTAL_PAGES.get(path)
        if portal_data:
            category = categories.filter(slug=portal_data[1]).first()
            breadcrumbs = [{'title': portal_data[0], 'href': path}]
            return (category, breadcrumbs)
        elif path.startswith(JOURNEY_PATHS):
            category = categories.filter(slug='mortgages').first() \
                or categories.first()
            breadcrumbs = get_journey_breadcrumbs(request, path)
            return (category, breadcrumbs)
        else:
            match = re.search(r'ask-cfpb/category-([A-Za-z0-9-_]*)/', path)
            if match.group(1):
                category = categories.filter(slug=match.group(1)).first()
                return (category, get_ask_breadcrumbs(category))
    except Exception:
        pass

    category = categories.first()
    breadcrumbs = get_ask_breadcrumbs(category)
    return (category, breadcrumbs)


def validate_page_number(request, paginator):
    """
    A utility for parsing a pagination request,
    catching invalid page numbers and always returning
    a valid page number, defaulting to 1.
    """
    raw_page = request.GET.get('page', 1)
    try:
        page_number = int(raw_page)
    except ValueError:
        page_number = 1
    try:
        paginator.page(page_number)
    except InvalidPage:
        page_number = 1
    return page_number


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


class SecondaryNavigationJSMixin(object):
    """A page mixin that adds navigation JS for English pages."""
    @property
    def page_js(self):
        js = super(SecondaryNavigationJSMixin, self).page_js
        if self.language == 'en':
            js += ['secondary-navigation.js']
        return js


class AnswerCategoryPage(RoutablePageMixin, SecondaryNavigationJSMixin,
                         CFGOVPage):
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
            'facets': facet_dict,
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
        context = self.get_context(request)
        paginator = Paginator(context.get('answers'), 20)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context.update({
            'paginator': paginator,
            'current_page': page_number,
            'questions': page,
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
        context = self.get_context(request)
        id_key = str(subcat.pk)
        answers = context['answers'].filter(
            pk__in=context['facets']['subcategories'][id_key])
        paginator = Paginator(answers, 20)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context.update({
            'paginator': paginator,
            'current_page': page_number,
            'results_count': answers.count(),
            'questions': page,
            'breadcrumb_items': get_ask_breadcrumbs(
                self.ask_category)
        })

        return TemplateResponse(
            request, self.get_template(request), context)


class AnswerResultsPage(SecondaryNavigationJSMixin, CFGOVPage):

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

    def get_context(self, request, **kwargs):

        context = super(
            AnswerResultsPage, self).get_context(request, **kwargs)
        context.update(**kwargs)
        paginator = Paginator(self.answers, 20)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context['current_page'] = page_number
        context['paginator'] = paginator
        context['results'] = page
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


class AnswerAudiencePage(SecondaryNavigationJSMixin, CFGOVPage):
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

    def get_context(self, request, *args, **kwargs):
        from ask_cfpb.models import Answer
        context = super(AnswerAudiencePage, self).get_context(request)
        answers = Answer.objects.filter(audiences__id=self.ask_audience.id)
        paginator = Paginator(answers, 20)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context.update({
            'answers': page,
            'current_page': page_number,
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

    def get_template(self, request):
        if self.language == 'es':
            return 'ask-cfpb/answer-tag-spanish-results.html'
        else:
            return 'ask-cfpb/answer-search-results.html'

    @route(r'^$')
    def tag_base(self, request):
        raise Http404

    @route(r'^(?P<tag>[^/]+)/$')
    def tag_search(self, request, **kwargs):
        from ask_cfpb.models import Answer
        tag_dict = Answer.valid_tags(language=self.language)
        tag = kwargs.get('tag').replace('_', ' ')
        if not tag or tag not in tag_dict['valid_tags']:
            raise Http404
        if self.language == 'es':
            self.answers = [
                (SPANISH_ANSWER_SLUG_BASE.format(a.id),
                 a.question_es,
                 Truncator(a.answer_es).words(40, truncate=' ...'))
                for a in tag_dict['tag_map'][tag]
                if a.answer_pages.filter(language='es', live=True)
            ]
        else:
            self.answers = [
                (ENGLISH_ANSWER_SLUG_BASE.format(a.id),
                 a.question,
                 Truncator(a.answer).words(40, truncate=' ...'))
                for a in tag_dict['tag_map'][tag]
                if a.answer_pages.filter(language='en', live=True)
            ]
        paginator = Paginator(self.answers, 20)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context = self.get_context(request)
        context['current_page'] = page_number
        context['results'] = page
        context['results_count'] = len(self.answers)
        context['tag'] = tag
        context['paginator'] = paginator
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

    sidebar = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('sidebar_contact', organisms.SidebarContactInfo()),
        ('rss_feed', molecules.RSSFeed()),
        ('social_media', molecules.SocialMedia()),
        ('reusable_text', v1_blocks.ReusableTextChooserBlock(ReusableText)),
    ], blank=True)

    sidebar_panels = [StreamFieldPanel('sidebar'), ]

    search_fields = Page.search_fields + [
        index.SearchField('question'),
        index.SearchField('answer'),
        index.SearchField('answer_base'),
        index.FilterField('language')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_panels, heading='Sidebar (English only)'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerPage, self).get_context(request)
        context['answer_id'] = self.answer_base.id
        context['related_questions'] = self.answer_base.related_questions.all()
        context['description'] = self.snippet if self.snippet \
            else Truncator(self.answer).words(40, truncate=' ...')
        context['audiences'] = [
            {'text': audience.name,
             'url': '/ask-cfpb/audience-{}'.format(
                    slugify(audience.name))}
            for audience in self.answer_base.audiences.all()]
        if self.language == 'es':
            tag_dict = self.Answer.valid_tags(language='es')
            context['tags_es'] = [tag for tag in self.answer_base.tags_es
                                  if tag in tag_dict['valid_tags']]
            context['tweet_text'] = Truncator(self.question).chars(
                100, truncate=' ...')
            context['disclaimer'] = get_reusable_text_snippet(
                SPANISH_DISCLAIMER_SNIPPET_TITLE)
            context['category'] = self.answer_base.category.first()
        elif self.language == 'en':
            # we're not using tags on English pages yet, so cut the overhead
            # tag_dict = self.Answer.valid_tags()
            # context['tags'] = [tag for tag in self.answer_base.tags
            #                    if tag in tag_dict['valid_tags']]
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['last_edited'] = self.answer_base.last_edited
            # breadcrumbs and/or category should reflect
            # the referrer if it is a consumer tools portal or
            # ask category page
            context['category'], context['breadcrumb_items'] = \
                get_question_referrer_data(
                    request, self.answer_base.category.all())
            subcategories = []
            for subcat in self.answer_base.subcategory.all():
                if subcat.parent == context['category']:
                    subcategories.append(subcat)
                for related in subcat.related_subcategories.all():
                    if related.parent == context['category']:
                        subcategories.append(related)
            context['subcategories'] = set(subcategories)

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
