import re
from collections import OrderedDict

from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.html import format_html, strip_tags
from django.utils.text import slugify
from django.utils.translation import activate, deactivate_all, gettext as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel,
    TabbedInterface
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable

from modelcluster.fields import ParentalKey

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models.answer_page import AnswerPage
from ask_cfpb.models.search import AnswerPageSearch
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models import (
    CFGOVPage, CFGOVPageManager, LandingPage, PortalCategory, PortalTopic,
    SublandingPage
)
from v1.models.snippets import ReusableText


REUSABLE_TEXT_TITLES = {
    'about_us': {
        'en': 'About us (For consumers)',
        'es': 'About us (for consumers) (in Spanish)'
    },
    'disclaimer': {
        'en': 'Legal disclaimer for consumer materials',
        'es': 'Legal disclaimer for consumer materials (in Spanish)'
    }
}


def get_standard_text(language, text_type):
    return get_reusable_text_snippet(
        REUSABLE_TEXT_TITLES[text_type][language]
    )


JOURNEY_PATHS = (
    '/owning-a-home/prepare',
    '/owning-a-home/explore',
    '/owning-a-home/compare',
    '/owning-a-home/close',
    '/owning-a-home/process',
)


def strip_html(markup):
    """Make sure stripping doesn't mash headings into text."""
    markup = re.sub("</h[1-6]>", " ", markup)
    return strip_tags(markup)


def get_reusable_text_snippet(snippet_title):
    try:
        return ReusableText.objects.get(
            title=snippet_title)
    except ReusableText.DoesNotExist:
        pass


def get_portal_or_portal_search_page(portal_topic, language='en'):
    if portal_topic:
        portal_page = portal_topic.portal_pages.filter(
            language=language, live=True).first()
        if portal_page:
            return portal_page
        else:
            portal_search_page = portal_topic.portal_search_pages.filter(
                language=language, live=True).first()
            return portal_search_page
    return None


def get_ask_breadcrumbs(language='en', portal_topic=None):
    DEFAULT_CRUMBS = {
        'es': [{
            'title': 'Obtener respuestas', 'href': '/es/obtener-respuestas/',
        }],
        'en': [{
            'title': 'Ask CFPB', 'href': '/ask-cfpb/',
        }],
    }
    if portal_topic:
        page = get_portal_or_portal_search_page(
            portal_topic=portal_topic, language=language)
        crumbs = [{
            'title': page.title,
            'href': page.url
        }]
        return crumbs
    return DEFAULT_CRUMBS[language]


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

    template = 'ask-cfpb/landing-page.html'

    objects = CFGOVPageManager()

    def get_portal_cards(self):
        """Return an array of dictionaries used to populate portal cards."""
        portal_cards = []
        portal_pages = SublandingPage.objects.filter(
            portal_topic_id__isnull=False,
            language=self.language,
        ).order_by('portal_topic__heading')
        for portal_page in portal_pages:
            topic = portal_page.portal_topic
            # Only include a portal if it has featured answers
            featured_answers = topic.featured_answers(self.language)
            if not featured_answers:
                continue
            # If the portal page is live, link to it
            if portal_page.live:
                url = portal_page.url
            # Otherwise, link to the topic "see all" page if there is one
            else:
                topic_page = topic.portal_search_pages.filter(
                    language=self.language,
                    live=True).first()
                if topic_page:
                    url = topic_page.url
                else:
                    continue  # pragma: no cover
            portal_cards.append({
                'topic': topic,
                'title': topic.title(self.language),
                'url': url,
                'featured_answers': featured_answers,
            })
        return portal_cards

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['portal_cards'] = self.get_portal_cards()
        context['about_us'] = get_standard_text(self.language, 'about_us')
        context['disclaimer'] = get_standard_text(self.language, 'disclaimer')
        return context


class SecondaryNavigationJSMixin:
    """A page mixin that adds navigation JS for English pages."""

    @property
    def page_js(self):
        js = super().page_js
        if self.language == 'en':
            js += ['secondary-navigation.js']
        return js


class PortalSearchPage(
        RoutablePageMixin, SecondaryNavigationJSMixin, CFGOVPage):
    """
    A routable page type for Ask CFPB portal search ("see-all") pages.
    """

    objects = CFGOVPageManager()
    portal_topic = models.ForeignKey(
        PortalTopic,
        blank=True,
        null=True,
        related_name='portal_search_pages',
        on_delete=models.SET_NULL)
    portal_category = None
    query_base = None
    glossary_terms = None
    category_slug = None
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
    def category_map(self):
        """
        Return an ordered dictionary of translated-slug:object pairs.

        We use this custom sequence for categories in the navigation sidebar,
        controlled by the 'display_order' field of portal categories:
        - Basics
        - Key terms
        - Common issues
        - Know your rights
        - How-to guides
        """
        categories = PortalCategory.objects.all()
        sorted_mapping = OrderedDict()
        for category in categories:
            sorted_mapping.update({
                slugify(
                    category.title(self.language)
                ): category
            })
        return sorted_mapping

    def results_message(self, count, heading, search_term):
        if search_term:
            _for_term = '{} "{}"'.format(_('for'), search_term)
        else:
            _for_term = ''
        if count == 1:
            _showing = _('Showing ')  # trailing space triggers singular es
            _results = _('result')
        else:
            _showing = _('Showing')
            _results = _('results')
        if self.portal_category and search_term:
            return format_html(
                '{} {} {} {} {} {}'
                '<span class="results-link"><a href="../?search_term={}">'
                '{} {}</a></span>',
                _showing,
                count,
                _results,
                _for_term,
                _('within'),
                heading.lower(),
                search_term,
                _('See all results within'),
                self.portal_topic.title(self.language).lower()
            )
        elif self.portal_category:
            return '{} {} {} {} {}'.format(
                _showing,
                count,
                _results,
                _('within'),
                heading.lower()
            )
        return '{} {} {} {} {} {}'.format(
            _showing,
            count,
            _results,
            _for_term,
            _('within'),
            heading.lower())

    def get_heading(self):
        if self.portal_category:
            return self.portal_category.title(self.language)
        else:
            return self.portal_topic.title(self.language)

    def get_context(self, request, *args, **kwargs):
        if self.language != 'en':
            activate(self.language)
        else:
            deactivate_all()
        return super().get_context(
            request, *args, **kwargs)

    def get_nav_items(self, request, page):
        """Return sorted nav items for sidebar."""
        sorted_categories = [
            {
                'title': category.title(self.language),
                'url': "{}{}/".format(page.url, slug),
                'active': (
                    False if not page.portal_category
                    else category.title(self.language)
                    == page.portal_category.title(self.language))
            }
            for slug, category in self.category_map.items()
        ]
        return [{
            'title': page.portal_topic.title(self.language),
            'url': page.url,
            'active': False if page.portal_category else True,
            'expanded': True,
            'children': sorted_categories
        }], True

    def get_results(self, request):
        context = self.get_context(request)
        search_term = request.GET.get('search_term', '').strip()
        search = AnswerPageSearch(
            search_term=search_term,
            base_query=self.query_base,
            language=self.language)
        response = search.search()
        if not response['results']:
            response = search.suggest()
        results = response['results']
        search_message = self.results_message(
            len(response['results']),
            self.get_heading(),
            search.search_term)
        paginator = Paginator(results, 25)
        page_number = validate_page_number(request, paginator)
        context.update({
            'search_term': search.search_term,
            'results_message': search_message,
            'pages': paginator.page(page_number),
            'paginator': paginator,
            'current_page': page_number,
            'get_secondary_nav_items': self.get_nav_items,
        })
        return TemplateResponse(
            request,
            'ask-cfpb/see-all.html',
            context)

    def get_glossary_terms(self):
        if self.language == 'es':
            terms = self.portal_topic.glossary_terms.order_by('name_es')
        else:
            terms = self.portal_topic.glossary_terms.order_by('name_en')
        for term in terms:
            if term.name(self.language) and term.definition(self.language):
                yield term

    @route(r'^$')
    def portal_topic_page(self, request):
        self.portal_category = None
        self.query_base = AnswerPageDocument.search().filter(
            'match', portal_topics=self.portal_topic.heading)
        return self.get_results(request)

    @route(r'^(?P<category>[^/]+)/$')
    def portal_category_page(self, request, **kwargs):
        self.category_slug = kwargs.get('category')
        if self.category_slug not in self.category_map:
            raise Http404
        self.portal_category = self.category_map.get(self.category_slug)
        self.title = "{} {}".format(
            self.portal_topic.title(self.language),
            self.portal_category.title(self.language).lower())
        if self.portal_category.heading == 'Key terms':
            self.glossary_terms = self.get_glossary_terms()
            context = self.get_context(request)
            context.update({
                'get_secondary_nav_items': self.get_nav_items})
            return TemplateResponse(
                request,
                'ask-cfpb/see-all.html',
                context)
        self.query_base = AnswerPageDocument.search().filter(
            'match', portal_topics=self.portal_topic.heading).filter(
            'match', portal_categories=self.portal_category.heading)
        return self.get_results(request)


class AnswerResultsPage(CFGOVPage):

    objects = CFGOVPageManager()
    answers = []

    edit_handler = TabbedInterface([
        ObjectList(CFGOVPage.content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'ask-cfpb/answer-search-results.html'

    def get_context(self, request, **kwargs):
        context = super(
            AnswerResultsPage, self).get_context(request, **kwargs)
        context.update(**kwargs)
        paginator = Paginator(self.answers, 25)
        page_number = validate_page_number(request, paginator)
        results = paginator.page(page_number)
        context['current_page'] = page_number
        context['paginator'] = paginator
        context['results'] = results
        context['results_count'] = len(self.answers)
        context['breadcrumb_items'] = get_ask_breadcrumbs(
            language=self.language)
        context['about_us'] = get_standard_text(self.language, 'about_us')
        context['disclaimer'] = get_standard_text(self.language, 'disclaimer')
        return context


class TagResultsPage(RoutablePageMixin, AnswerResultsPage):
    """A routable page for serving Answers by tag"""

    template = 'ask-cfpb/answer-search-results.html'

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        if self.language != 'en':
            activate(self.language)
        else:
            deactivate_all()
        context = super(
            TagResultsPage, self).get_context(request, *args, **kwargs)
        return context

    @route(r'^$')
    def tag_base(self, request):
        raise Http404

    @route(r'^(?P<tag>[^/]+)/$')
    def tag_search(self, request, **kwargs):
        """
        Return results as a list of 3-tuples: (url, question, answer-preview).

        This matches the result form used for /ask-cfpb/search/ queries,
        which use the same template but deliver results from Elasticsearch.
        """
        tag = kwargs.get('tag').replace('_', ' ')
        base_query = AnswerPage.objects.filter(
            language=self.language,
            redirect_to_page=None,
            live=True)
        answer_tuples = [
            (page.url, page.question, page.answer_content_preview())
            for page in base_query if tag in page.clean_search_tags
        ]
        paginator = Paginator(answer_tuples, 25)
        page_number = validate_page_number(request, paginator)
        page = paginator.page(page_number)
        context = self.get_context(request)
        context['current_page'] = page_number
        context['results'] = page
        context['results_count'] = len(answer_tuples)
        context['tag'] = tag
        context['paginator'] = paginator
        return TemplateResponse(
            request,
            self.template,
            context)


class ArticleLink(Orderable, models.Model):
    text = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    article_page = ParentalKey(
        'ArticlePage',
        related_name='article_links'
    )

    panels = [
        FieldPanel('text'),
        FieldPanel('url'),
    ]


class ArticlePage(CFGOVPage):
    """
    General article page type.
    """
    category = models.CharField(
        choices=[
            ('basics', 'Basics'),
            ('common_issues', 'Common issues'),
            ('howto', 'How to'),
            ('know_your_rights', 'Know your rights'),
        ],
        max_length=255,
    )
    heading = models.CharField(
        max_length=255,
        blank=False,
    )
    intro = models.TextField(
        blank=False
    )
    inset_heading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Heading"
    )
    sections = StreamField([
        ('section', blocks.StructBlock([
            ('heading', blocks.CharBlock(
                max_length=255,
                required=True,
                label='Section heading'
            )),
            ('summary', blocks.TextBlock(
                required=False,
                blank=True,
                label='Section summary'
            )),
            ('link_text', blocks.CharBlock(
                required=False,
                blank=True,
                label="Section link text"
            )),
            ('url', blocks.CharBlock(
                required=False,
                blank=True,
                label='Section link URL',
                max_length=255,
            )),
            ('subsections', blocks.ListBlock(
                blocks.StructBlock([
                    ('heading', blocks.CharBlock(
                        max_length=255,
                        required=False,
                        blank=True,
                        label='Subsection heading'
                    )),
                    ('summary', blocks.TextBlock(
                        required=False,
                        blank=True,
                        label='Subsection summary'
                    )),
                    ('link_text', blocks.CharBlock(
                        required=True,
                        label='Subsection link text'
                    )),
                    ('url', blocks.CharBlock(
                        required=True,
                        label='Subsection link URL'
                    ))
                ])
            ))
        ]))
    ])
    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('heading'),
            FieldPanel('intro')],
            heading="Heading",
            classname="collapsible"),

        MultiFieldPanel([
            FieldPanel('inset_heading'),
            InlinePanel(
                'article_links',
                label='Inset link',
                max_num=2
            ), ],
            heading="Inset links",
            classname="collapsible"),

        StreamFieldPanel('sections'),
    ]

    sidebar = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('reusable_text', v1_blocks.ReusableTextChooserBlock(ReusableText)),
    ], blank=True)

    sidebar_panels = [StreamFieldPanel('sidebar'), ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'ask-cfpb/article-page.html'

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['about_us'] = get_standard_text(self.language, 'about_us')
        return context

    def __str__(self):
        return self.title
