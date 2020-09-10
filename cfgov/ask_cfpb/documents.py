from django import forms
from django.db import models
from django.utils.html import strip_tags

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from elasticsearch_dsl import analyzer, tokenizer, token_filter

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel,
    TabbedInterface
)
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel

from ask_cfpb.models import blocks as ask_blocks
from ask_cfpb.search_indexes import extract_raw_text, truncatissimo as truncate

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models import CFGOVPage, CFGOVPageManager, PortalCategory, PortalTopic
from v1.models.snippets import RelatedResource, ReusableText

label_autocomplete = analyzer(
    'label_autocomplete',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=2, max_gram=25, token_chars=["letter", "digit"]),
    filter=['lowercase', token_filter('ascii_fold', 'asciifolding')]
)

synonynm_filter = token_filter(
    'synonym_filter_en',
    'synonym',
    synonyms_path = '/usr/share/elasticsearch/config/synonyms/synonyms_en.txt'
)

synonym_analyzer = analyzer(
    'synonym_analyzer_en',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])

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

def get_reusable_text_snippet(snippet_title):
    try:
        return ReusableText.objects.get(
            title=snippet_title)
    except ReusableText.DoesNotExist:
        pass

def get_standard_text(language, text_type):
    return get_reusable_text_snippet(
        REUSABLE_TEXT_TITLES[text_type][language]
    )

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

    share_and_print = models.BooleanField(
        default=False,
        help_text="Include share and print buttons above page content."
    )

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('last_edited'),
            FieldPanel('question'),
            FieldPanel('statement'),
            FieldPanel('short_answer')],
            heading="Page content",
            classname="collapsible"),
        FieldPanel('share_and_print'),
        StreamFieldPanel('answer_content'),
        MultiFieldPanel([
            SnippetChooserPanel('related_resource'),
            AutocompletePanel(
                'related_questions',
                target_model='ask_cfpb.AnswerPage')],
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
                'redirect_to_page', target_model='ask_cfpb.AnswerPage')],
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

    def answer_content_text(self):
        raw_text = extract_raw_text(self.answer_content.stream_data)
        return strip_tags(" ".join([self.short_answer, raw_text]))

    def answer_content_data(self):
        return truncate(self.answer_content_text())

    def short_answer_data(self):
        return ' '.join(RichTextField.get_searchable_content(self, self.short_answer))

    def text(self):
        short_answer = self.short_answer_data()
        answer_text = self.answer_content_text()
        full_text = short_answer + "\n\n" + answer_text + "\n\n" + self.question
        return full_text

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

@registry.register_document
class AnswerPageDocument(Document):

    autocomplete = fields.TextField(analyzer=label_autocomplete)
    portal_topics = fields.KeywordField()
    portal_categories = fields.TextField()
    text = fields.TextField(attr="text", analyzer=synonym_analyzer)
    url = fields.TextField()
    suggestions = fields.TextField(attr="text")
    preview = fields.TextField(attr="answer_content_data")


    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(live=True, redirect_to_page=None)

    def prepare_autocomplete(self, instance):
        return instance.question

    def prepare_portal_categories(self, instance):
        return [topic.heading for topic in instance.portal_category.all()]

    def prepare_portal_topics(self, instance):
        return [topic.heading for topic in instance.portal_topic.all()]

    def prepare_search_tags(self, instance):
        return instance.clean_search_tags

    def prepare_url(self, instance):
        return instance.url

    class Index:
        name = 'ask-cfpb'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
        
    class Django:
        model = AnswerPage

        fields = [
            'search_tags',
            'language',
        ]

UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term  

def get_suggestion_for_search(search_term):
    s = AnswerPageDocument.search().suggest('text_suggestion', search_term, term={'field': 'text'})
    response = s.execute()
    try:
        suggested_term = response.suggest.text_suggestion[0].options[0].text
        return suggested_term
    except IndexError:
        return search_term

class AnswerPageSearch:
    def __init__(self, search_term, language='en', base_query=None):
        self.language = language
        self.search_term = make_safe(search_term).strip()
        self.base_query = base_query

    def autocomplete(self):
        s = AnswerPageDocument.search().query('match', autocomplete=self.search_term)
        results = [{'question': result.autocomplete, 'url': result.url } for result in s[:20]]
        return results

    def search(self):
        if not self.base_query:
            search = AnswerPageDocument.search().filter("term", language=self.language)
        else:
            search = self.base_query.filter("term", language=self.language)
        
        if self.search_term != '':
            search.query("term", text=self.search_term)
        total_results = search.count()
        search = search[0:total_results]
        response = search.execute()
        results = response[0:total_results]
        return {
            'search_term': self.search_term,
            'suggestion': None,
            'results': results
        }

    def suggest(self):
        suggested_term = get_suggestion_for_search(self.search_term)
        if suggested_term != self.search_term:
            if not self.base_query:
                search = AnswerPageDocument.search()
            else:
                search = self.base_query
            suggested_results = search.query("term", text=suggested_term).filter("term", language=self.language)
            total = suggested_results.count()
            suggested_results = suggested_results[0:total]
            suggested_response = suggested_results.execute()
            results = suggested_response[0:total]
            return {
                'search_term': suggested_term,
                'suggestion': self.search_term,
                'results': results
            }
        else:
            # We know there are no results for the original term, so return an empty results list with no suggestion.
            return {
                'search_term': self.search_term,
                'suggestion': None,
                'results': []
            }
