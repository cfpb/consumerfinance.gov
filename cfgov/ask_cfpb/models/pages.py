from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from urllib.parse import unquote

from django import forms
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator, slugify
from django.utils.translation import activate, deactivate_all, gettext as _
from haystack.query import SearchQuerySet

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtailautocomplete.edit_handlers import AutocompletePanel

from ask_cfpb.models import blocks as ask_blocks
from ask_cfpb.models.search import AskSearch
from ask_cfpb.search_indexes import extract_raw_text, truncatissimo as truncate
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models import (
    CFGOVPage, CFGOVPageManager, LandingPage, PortalCategory, PortalTopic,
    SublandingPage
)
from v1.models.snippets import RelatedResource, ReusableText


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


def get_reusable_text_snippet(snippet_title):
    try:
        return ReusableText.objects.get(
            title=snippet_title)
    except ReusableText.DoesNotExist:
        pass


def get_answer_preview(page):
    """Extract an answer summary for use in search result previews."""
    raw_text = extract_raw_text(page.answer_content.stream_data)
    full_text = strip_tags(" ".join([page.short_answer, raw_text]))
    return truncate(full_text)


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
        context = super(AnswerLandingPage, self).get_context(request)
        context['portal_cards'] = self.get_portal_cards()
        context['about_us'] = get_standard_text(self.language, 'about_us')
        context['disclaimer'] = get_standard_text(self.language, 'disclaimer')
        return context


class SecondaryNavigationJSMixin(object):
    """A page mixin that adds navigation JS for English pages."""
    @property
    def page_js(self):
        js = super(SecondaryNavigationJSMixin, self).page_js
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
        return super(PortalSearchPage, self).get_context(
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
        if not search_term or len(unquote(search_term)) == 1:
            results = self.query_base
        else:
            search = AskSearch(
                search_term=search_term,
                query_base=self.query_base)
            results = search.queryset
            if results.count() == 0:
                # No results, so let's try to suggest a better query
                search.suggest(request=request)
                results = search.queryset
                search_term = search.search_term
        search_message = self.results_message(
            results.count(),
            self.get_heading(),
            search_term)
        paginator = Paginator(results, 10)
        page_number = validate_page_number(request, paginator)
        context.update({
            'search_term': search_term,
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
        self.query_base = SearchQuerySet().filter(
            portal_topics=self.portal_topic.heading,
            language=self.language)
        self.portal_category = None
        return self.get_results(request)

    @route(r'^(?P<category>[^/]+)/$')
    def portal_category_page(self, request, **kwargs):
        category_slug = kwargs.get('category')
        if category_slug not in self.category_map:
            raise Http404
        self.portal_category = self.category_map.get(category_slug)
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
        self.query_base = SearchQuerySet().filter(
            portal_topics=self.portal_topic.heading,
            language=self.language,
            portal_categories=self.portal_category.heading)
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
        paginator = Paginator(self.answers, 20)
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
        Return results as a ist of 3-tuples: (url, question, answer-preview).

        This matches the result form used for /ask-cfpb/search/ queries,
        which use the same template but deliver results from Elasticsearch.
        """
        tag = kwargs.get('tag').replace('_', ' ')
        base_query = AnswerPage.objects.filter(
            language=self.language,
            redirect_to_page=None,
            live=True)
        answer_tuples = [
            (page.url, page.question, get_answer_preview(page))
            for page in base_query if tag in page.clean_search_tags
        ]
        paginator = Paginator(answer_tuples, 20)
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


class AnswerPage(CFGOVPage):
    """Page type for Ask CFPB answers."""
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
        blank=True,
        features=['link', 'document-link'],
        help_text='Optional answer intro')
    answer_content = StreamField(
        ask_blocks.AskAnswerContent(),
        blank=True,
        verbose_name='Answer')
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
            FieldPanel('short_answer')],
            heading="Page content",
            classname="collapsible"),
        StreamFieldPanel('answer_content'),
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
            FieldPanel('featured')],
            heading="Featured answer on Ask landing page",
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
        index.SearchField('answer_content'),
        index.SearchField('short_answer')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'ask-cfpb/answer-page.html'

    objects = CFGOVPageManager()

    def get_sibling_url(self):
        if self.answer_base:
            if self.language == 'es':
                sibling = self.answer_base.english_page
            else:
                sibling = self.answer_base.spanish_page
            if sibling and sibling.live and not sibling.redirect_to_page:
                return sibling.url

    def get_context(self, request, *args, **kwargs):
        portal_topic = self.primary_portal_topic or self.portal_topic.first()
        context = super(AnswerPage, self).get_context(request)
        context['related_questions'] = self.related_questions.all()
        context['description'] = (
            self.short_answer if self.short_answer
            else Truncator(self.answer_content).words(40, truncate=' ...'))
        context['last_edited'] = self.last_edited
        context['portal_page'] = get_portal_or_portal_search_page(
            portal_topic, language=self.language)
        context['breadcrumb_items'] = get_ask_breadcrumbs(
            language=self.language,
            portal_topic=portal_topic,
        )
        context['about_us'] = get_standard_text(self.language, 'about_us')
        context['disclaimer'] = get_standard_text(self.language, 'disclaimer')
        context['sibling_url'] = self.get_sibling_url()
        return context

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


@python_2_unicode_compatible
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

    search_fields = Page.search_fields + [
        index.SearchField('title'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'ask-cfpb/article-page.html'

    objects = CFGOVPageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(ArticlePage, self).get_context(request)
        context['about_us'] = get_standard_text(self.language, 'about_us')
        return context

    def __str__(self):
        return self.title
