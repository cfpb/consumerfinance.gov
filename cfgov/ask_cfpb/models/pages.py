from __future__ import absolute_import, unicode_literals

import re
from six.moves.urllib.parse import urlparse, unquote

from django import forms
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.text import Truncator, slugify
from django.utils.translation import activate, deactivate_all
from django.utils.translation import gettext as _

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from flags.state import flag_enabled
from haystack.query import SearchQuerySet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtailautocomplete.edit_handlers import AutocompletePanel

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models import (
    CFGOVPage, CFGOVPageManager, LandingPage, PortalCategory, PortalTopic
)
from v1.models.snippets import RelatedResource, ReusableText


LANGUAGE_BASES = {
    'es': '/es/obtener-respuestas/{}/',
    'en': '/ask-cfpb/{}/'
}
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


class SeeAllPage(RoutablePageMixin, SecondaryNavigationJSMixin, CFGOVPage):
    """
    A routable page type for Ask CFPB portal seearch pages.
    """

    objects = CFGOVPageManager()
    portal_topic = models.ForeignKey(
        PortalTopic,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    portal_category = None
    overview = models.TextField(blank=True)
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('portal_topic'),
        FieldPanel('overview'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    @property
    def query_base(self):
        return SearchQuerySet().filter(
            portal_topics=self.portal_topic.heading,
            language=self.language)

    @property
    def category_map(self):
        return {
            slugify(_(category.heading)): category
            for category in PortalCategory.objects.all()
        }

    def results_message(self, count, heading, search_term):
        if count == 0 and self.portal_category:
            return format_html(
                '{} {} {} {}<br><p><a href="../?search_term={}">'
                'Search all {} answers</a></p>',
                _('Showing'),
                count,
                _('answers within'),
                heading.lower(),
                search_term,
                _(self.portal_topic.heading)
            )
        return '{} {} {} {}'.format(
            _('Showing'),
            count,
            _('answers within'),
            heading.lower())

    def get_template(self, request):
        return 'ask-cfpb/see-all.html'

    def get_heading(self, obj):
        if self.language == 'es':
            return obj.heading_es
        else:
            return obj.heading

    def get_context(self, request, *args, **kwargs):
        if self.language != 'en':
            activate(self.language)
        else:
            deactivate_all()
        return super(SeeAllPage, self).get_context(request, *args, **kwargs)

    def get_nav_items(self, request, page):
        """Return nav items sorted by an arbitrary order."""
        search_term = request.GET.get('search_term', '').strip()
        pk_sort_order = [1, 4, 5, 2, 3]
        hand_sorted_categories = []
        for pk in pk_sort_order:
            category = PortalCategory.objects.get(pk=pk)
            hand_sorted_categories.append({
                'title': _(category.heading),
                'url': ("{}{}/?search_term={}".format(
                    page.url,
                    slugify(_(category.heading)),
                    search_term)),
                'active': (
                    False if not page.portal_category
                    else _(category.heading)
                    == _(page.portal_category.heading)),
            })
        return [{
            'title': _(page.portal_topic.heading),
            'url': "{}?search_term={}".format(page.url, search_term),
            'active': False if page.portal_category else True,
            'expanded': True,
            'children': hand_sorted_categories
        }], True

    @route(r'^$')
    def portal_topic_page(self, request):
        context = self.get_context(request)
        heading = self.get_heading(self.portal_topic)
        context['heading'] = heading
        search_term = request.GET.get('search_term', '').strip()
        if not search_term or len(unquote(search_term)) == 1:
            count = self.query_base.count()
            sqs = self.query_base
            search_message = self.results_message(count, heading, search_term)
        else:
            sqs = self.query_base.filter(content=search_term)
            count = sqs.count()
            if count == 0:
                # No results, so let's try to suggest a better query
                suggestion = SearchQuerySet().models(
                    AnswerPage).spelling_suggestion(search_term)
                if suggestion == search_term:
                    suggestion = None
                elif (request.GET.get('correct', '1') == '1' and
                        flag_enabled('ASK_SEARCH_TYPOS', request=request)):
                    sqs = self.query_base.filter(content=suggestion)
                    search_term, suggestion = suggestion, search_term
                    count = sqs.count()
            context['pages'] = sqs
            search_message = self.results_message(count, heading, search_term)
        paginator = Paginator(sqs, 10)
        page_number = validate_page_number(request, paginator)
        pages = paginator.page(page_number)
        context.update({
            'count': count,
            'search_term': search_term,
            'results_message': search_message,
            'pages': pages,
            'paginator': paginator,
            'current_page': page_number,
            'get_secondary_nav_items': self.get_nav_items,
        })
        return TemplateResponse(
            request,
            self.get_template(request),
            context)

    @route(r'^(?P<category>[^/]+)/$')
    def portal_category_page(self, request, **kwargs):
        context = self.get_context(request)
        category_slug = kwargs.get('category')
        self.portal_category = self.category_map.get(category_slug)
        heading = self.get_heading(self.portal_category)
        sqs = self.query_base.filter(
            portal_categories=self.portal_category.heading)
        search_term = request.GET.get('search_term', '').strip()
        if not search_term or len(unquote(search_term)) == 1:
            count = sqs.count()
            search_message = self.results_message(count, heading, search_term)
        else:
            sqs = sqs.filter(content=search_term)
            count = sqs.count()
            if count == 0:
                # No results, so let's try to suggest a better query
                suggestion = SearchQuerySet().models(
                    AnswerPage).spelling_suggestion(search_term)
                if suggestion == search_term:
                    suggestion = None
                elif (request.GET.get('correct', '1') == '1' and
                        flag_enabled('ASK_SEARCH_TYPOS', request=request)):
                    sqs = self.query_base.filter(content=suggestion)
                    search_term, suggestion = suggestion, search_term
                    count = sqs.count()
            search_message = self.results_message(count, heading, search_term)
        paginator = Paginator(sqs, 10)
        page_number = validate_page_number(request, paginator)
        pages = paginator.page(page_number)
        context.update({
            'count': count,
            'heading': heading,
            'search_term': search_term,
            'results_message': search_message,
            'pages': pages,
            'paginator': paginator,
            'current_page': page_number,
            'get_secondary_nav_items': self.get_nav_items,
        })
        return TemplateResponse(
            request,
            self.get_template(request),
            context)


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
        answers = self.ask_category.answerpage_set.filter(
            language=self.language, redirect_to_page=None, live=True).values(
                'answer_base__id', 'question', 'slug', 'answer')
        if self.language == 'es':
            for a in answers:
                a['answer'] = Truncator(a['answer']).words(
                    40, truncate=' ...')
        subcats = self.ask_category.subcategories.all()
        context.update({
            'answers': answers,
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
            context['search_tags'] = self.ask_category.top_tags
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
        answers = self.ask_subcategory.answerpage_set.filter(
            language=self.language, live=True, redirect_to_page=None)
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
        tag = kwargs.get('tag').replace('_', ' ')
        self.answers = AnswerPage.objects.filter(
            language=self.language,
            search_tags__contains=tag,
            redirect_to_page=None,
            live=True)
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
    last_edited = models.DateField(
        blank=True,
        null=True,
        help_text="Change the date to today if you make a significant change.")
    question = models.TextField(blank=True)
    statement = models.TextField(
        blank=True,
        help_text=(
            "(Optional) Use this field to rephrase the question title as "
            "a statement. Use only if this answer has been chosen to appear "
            "on a money topic portal (e.g. /consumer-tools/debt-collection)."))
    short_answer = RichTextField(
        blank=True, help_text='Optional answer intro')
    answer = RichTextField(
        blank=True,
        features=[
            'bold', 'italic', 'h2', 'h3', 'h4', 'link', 'ol', 'ul',
            'document-link', 'image', 'embed', 'ask-tips', 'edit-html'
        ],
        help_text=(
            "Do not use H2 or H3 to style text. Only use the HTML Editor "
            "for troubleshooting. To style tips, warnings and notes, "
            "select the content that will go inside the rule lines "
            "(so, title + paragraph) and click the Pencil button "
            "to style it. Re-select the content and click the button "
            "again to unstyle the tip."
        )
    )
    answer_base = models.ForeignKey(
        Answer,
        blank=True,
        null=True,
        related_name='answer_pages',
        on_delete=models.SET_NULL)
    redirect_to_page = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='redirect_to_pages',
        help_text="Choose another AnswerPage to redirect this page to")
    featured = models.BooleanField(
        default=False,
        help_text=(
            "Check to make this one of two featured answers "
            "on the landing page."))
    featured_rank = models.IntegerField(blank=True, null=True)
    category = models.ManyToManyField(
        'Category',
        blank=True,
        help_text=(
            "Categorize this answer. "
            "Avoid putting into more than one category."))
    subcategory = models.ManyToManyField(
        'SubCategory',
        blank=True,
        help_text=(
            "Choose only subcategories that belong "
            "to one of the categories checked above."))
    search_tags = models.CharField(
        max_length=1000,
        blank=True,
        help_text="Search words or phrases, separated by commas")
    related_resource = models.ForeignKey(
        RelatedResource,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    related_questions = ParentalManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='related_question',
        help_text='Maximum of 3 related questions')
    portal_topic = ParentalManyToManyField(
        PortalTopic,
        blank=True,
        help_text='Limit to 1 portal topic if possible')
    primary_portal_topic = ParentalKey(
        PortalTopic,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='primary_portal_topic',
        help_text=(
            "Use only if assigning more than one portal topic, "
            "to control which topic is used as a breadcrumb."))
    portal_category = ParentalManyToManyField(
        PortalCategory,
        blank=True)

    user_feedback = StreamField([
        ('feedback', v1_blocks.Feedback()),
    ], blank=True)

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('last_edited'),
            FieldPanel('question'),
            FieldPanel('statement'),
            FieldPanel('short_answer'),
            FieldPanel('answer')],
            heading="Page content",
            classname="collapsible"),
        MultiFieldPanel([
            SnippetChooserPanel('related_resource'),
            AutocompletePanel(
                'related_questions',
                page_type='ask_cfpb.AnswerPage',
                is_single=False)],
            heading="Related resources",
            classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('portal_topic', widget=forms.CheckboxSelectMultiple),
            FieldPanel('primary_portal_topic'),
            FieldPanel(
                'portal_category', widget=forms.CheckboxSelectMultiple)],
            heading="Portal tags",
            classname="collapsible"),
        MultiFieldPanel([
            AutocompletePanel(
                'redirect_to_page', page_type='ask_cfpb.AnswerPage')],
            heading="Redirect to another answer",
            classname="collapsible"),
        MultiFieldPanel([
            StreamFieldPanel('user_feedback')],
            heading="User feedback",
            classname="collapsible collapsed"),
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
        index.SearchField('answer'),
        index.SearchField('short_answer')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_panels, heading='Sidebar (English only)'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerPage, self).get_context(request)
        context['related_questions'] = self.related_questions.all()
        context['description'] = self.short_answer if self.short_answer \
            else Truncator(self.answer).words(40, truncate=' ...')
        context['answer_id'] = self.answer_base.id
        if self.language == 'es':
            context['search_tags'] = self.clean_search_tags
            context['tweet_text'] = Truncator(self.question).chars(
                100, truncate=' ...')
            context['disclaimer'] = get_reusable_text_snippet(
                SPANISH_DISCLAIMER_SNIPPET_TITLE)
            context['category'] = self.category.first()
        elif self.language == 'en':
            context['about_us'] = get_reusable_text_snippet(
                ABOUT_US_SNIPPET_TITLE)
            context['disclaimer'] = get_reusable_text_snippet(
                ENGLISH_DISCLAIMER_SNIPPET_TITLE)
            context['last_edited'] = self.last_edited
            # breadcrumbs and/or category should reflect
            # the referrer if it is a consumer tools portal or
            # ask category page
            context['category'], context['breadcrumb_items'] = \
                get_question_referrer_data(
                    request, self.category.all())
            subcategories = []
            for subcat in self.subcategory.all():
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
    def clean_search_tags(self):
        return [
            tag.strip()
            for tag in self.search_tags.split(',')
        ]

    @property
    def status_string(self):
        if self.redirect_to_page:
            if not self.live:
                return ("redirected but not live")
            else:
                return ("redirected")
        else:
            return super(AnswerPage, self).status_string

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        if self.social_sharing_image:
            return self.social_sharing_image

        if not self.category.exists():
            return None

        return self.category.first().category_image

    # Overrides the default of page.id for comparing against split testing
    # clusters. See: core.feature_flags.in_split_testing_cluster
    @property
    def split_test_id(self):
        return self.answer_base.id
