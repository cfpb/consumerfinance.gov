from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from search.elasticsearch_helpers import (
    environment_specific_index, ngram_tokenizer
)
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.learn_page import (
    AbstractFilterPage, DocumentDetailPage, EventPage, LearnPage
)
from v1.models.newsroom_page import LegacyNewsroomPage, NewsroomPage


@registry.register_document
class FilterablePagesDocument(Document):

    tags = fields.ObjectField(properties={
        'slug': fields.KeywordField()
    })
    categories = fields.ObjectField(properties={
        'name': fields.KeywordField()
    })
    authors = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.KeywordField()
    })
    title = fields.TextField(attr='title', analyzer=ngram_tokenizer)
    is_archived = fields.KeywordField(attr='is_archived')
    date_published = fields.DateField(attr='date_published')
    url = fields.KeywordField()
    start_dt = fields.DateField()
    end_dt = fields.DateField()
    statuses = fields.KeywordField()
    products = fields.KeywordField()
    initial_filing_date = fields.DateField()
    model_class = fields.KeywordField()

    def get_queryset(self):
        return AbstractFilterPage.objects.live().public().specific()

    def prepare_url(self, instance):
        return instance.url

    def prepare_start_dt(self, instance):
        return getattr(instance, 'start_dt', None)

    def prepare_end_dt(self, instance):
        return getattr(instance, 'end_dt', None)

    def prepare_statuses(self, instance):
        statuses = getattr(instance, 'statuses', None)
        if statuses is not None:
            return [status.status for status in statuses.all()]
        else:
            return None

    def prepare_products(self, instance):
        products = getattr(instance, 'products', None)
        if products is not None:
            return [p.product for p in products.all()]
        else:
            return None

    def prepare_initial_filing_date(self, instance):
        return getattr(instance, 'initial_filing_date', None)

    def prepare_model_class(self, instance):
        return instance.__class__.__name__

    def get_instances_from_related(self, related_instance):
        # Related instances all inherit from AbstractFilterPage.
        return related_instance

    class Django:
        model = AbstractFilterPage

        related_models = [
            BlogPage,
            DocumentDetailPage,
            EnforcementActionPage,
            EventPage,
            LearnPage,
            LegacyBlogPage,
            LegacyNewsroomPage,
            NewsroomPage
        ]

    class Index:
        name = environment_specific_index('filterable-pages')


class FilterablePagesDocumentSearch:

    def __init__(self,
                 prefix='/', topics=[], categories=[],
                 authors=[], to_date=None, from_date=None,
                 title='', archived=None):
        self.prefix = prefix
        self.topics = topics
        self.categories = categories
        self.authors = authors
        self.to_date = to_date
        self.from_date = from_date
        self.title = title
        self.archived = archived

    def filter_topics(self, search):
        return search.filter("terms", tags__slug=self.topics)

    def filter_categories(self, search):
        return search.filter("terms", categories__name=self.categories)

    def filter_authors(self, search):
        return search.filter("terms", authors__slug=self.authors)

    def filter_date(self, search):
        return search.filter(
            "range", **{
                'date_published': {
                    'gte': self.from_date, 'lte': self.to_date}})

    def filter_archived(self, search):
        return search.filter("terms", is_archived=self.archived)

    def search_title(self, search):
        return search.query(
            "match", title={"query": self.title, "operator": "AND"}
        )

    def order_results(self, search):
        total_results = search.count()
        return search.sort('-date_published')[0:total_results]

    def has_dates(self):
        return self.to_date is not None and self.from_date is not None

    def apply_specific_filters(self, search):
        return search

    def search(self):
        search = FilterablePagesDocument.search()
        if self.prefix != '':
            search = search.filter('prefix', url=self.prefix)
        if self.topics not in ([], '', None):
            search = self.filter_topics(search)
        if self.categories not in ([], '', None):
            search = self.filter_categories(search)
        if self.authors not in ([], '', None):
            search = self.filter_authors(search)
        if self.has_dates():
            search = self.filter_date(search)
        if self.archived is not None:
            search = self.filter_archived(search)
        if self.title not in ([], '', None):
            search = self.search_title(search)

        search = self.apply_specific_filters(search)
        results = self.order_results(search)
        return results.to_queryset()


class EventFilterablePagesDocumentSearch(FilterablePagesDocumentSearch):

    def filter_date(self, search):
        return search.filter(
            "range", **{
                'start_dt': {'gte': self.from_date}}).filter(
                    "range", **{'end_dt': {'lte': self.to_date}})

    def apply_specific_filters(self, search):
        return search.filter("term", model_class="EventPage")


class EnforcementActionFilterablePagesDocumentSearch(FilterablePagesDocumentSearch):  # noqa: E501

    def __init__(self, **kwargs):
        self.statuses = kwargs.pop('statuses')
        self.products = kwargs.pop('products')
        super().__init__(**kwargs)

    def filter_date(self, search):
        return search.filter(
            "range", **{
                "initial_filing_date": {
                    "gte": self.from_date, "lte": self.to_date}})

    def apply_specific_filters(self, search):
        search = search.filter("term", model_class="EnforcementActionPage")
        if self.statuses != []:
            search = search.filter("terms", statuses=self.statuses)
        if self.products != []:
            search = search.filter("terms", products=self.products)

        return search

    def order_results(self, search):
        total_results = search.count()
        return search.sort('-initial_filing_date')[0:total_results]
