from html import unescape

from django.core.exceptions import FieldDoesNotExist
from django.utils.html import strip_tags

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import A
from elasticsearch_dsl.query import MultiMatch

from search.elasticsearch_helpers import environment_specific_index
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.learn_page import (
    AbstractFilterPage,
    DocumentDetailPage,
    EventPage,
    LearnPage,
)
from v1.models.newsroom_page import LegacyNewsroomPage, NewsroomPage


@registry.register_document
class FilterablePagesDocument(Document):

    tags = fields.ObjectField(
        properties={"slug": fields.KeywordField(), "name": fields.TextField()}
    )
    categories = fields.ObjectField(properties={"name": fields.KeywordField()})
    language = fields.KeywordField()

    title = fields.TextField(attr="title")
    is_archived = fields.KeywordField(attr="is_archived")
    date_published = fields.DateField(attr="date_published")
    url = fields.KeywordField()
    start_dt = fields.DateField()
    end_dt = fields.DateField()
    statuses = fields.KeywordField()
    products = fields.KeywordField()
    initial_filing_date = fields.DateField()
    model_class = fields.KeywordField()
    content = fields.TextField()
    preview_description = fields.TextField()
    path = fields.TextField()
    depth = fields.IntegerField()

    def get_queryset(self):
        return AbstractFilterPage.objects.live().public().specific()

    def prepare_url(self, instance):
        return instance.url

    def prepare_start_dt(self, instance):
        return getattr(instance, "start_dt", None)

    def prepare_end_dt(self, instance):
        return getattr(instance, "end_dt", None)

    def prepare_statuses(self, instance):
        statuses = getattr(instance, "statuses", None)
        if statuses is not None:
            return [status.status for status in statuses.all()]
        else:
            return None

    def prepare_products(self, instance):
        products = getattr(instance, "products", None)
        if products is not None:
            return [p.product for p in products.all()]
        else:
            return None

    def prepare_initial_filing_date(self, instance):
        return getattr(instance, "initial_filing_date", None)

    def prepare_model_class(self, instance):
        return instance.__class__.__name__

    def prepare_content(self, instance):
        try:
            content_field = instance._meta.get_field("content")
            value = content_field.value_from_object(instance)
            content = content_field.get_searchable_content(value)
            content = content.pop()
            return content
        except FieldDoesNotExist:
            return None
        except IndexError:
            return None

    def prepare_preview_description(self, instance):
        return unescape(strip_tags(instance.preview_description))

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
            NewsroomPage,
        ]

    class Index:
        name = environment_specific_index("filterable-pages")
        settings = {"index.max_ngram_diff": 23}


class FilterablePagesDocumentSearch:
    def __init__(self, prefix="/"):
        self.prefix = prefix
        self.document = FilterablePagesDocument()
        self.search_obj = self.document.search().filter("prefix", url=prefix)

    def filter_topics(self, topics=None):
        if topics is None:
            topics = []
        if topics not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", tags__slug=topics
            )

    def filter_categories(self, categories=None):
        if categories is None:
            categories = []
        if categories not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", categories__name=categories
            )

    def filter_language(self, language=None):
        if language is None:
            language = []
        if language not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", language=language
            )

    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range",
                **{"date_published": {"gte": from_date, "lte": to_date}},
            )

    def filter_archived(self, archived=None):
        if archived is not None:
            self.search_obj = self.search_obj.filter(
                "terms", is_archived=archived
            )

    def search_title(self, title=""):
        if title not in ([], "", None):
            query = MultiMatch(
                query=title,
                fields=[
                    "title^10",
                    "tags.name^10",
                    "content",
                    "preview_description",
                ],
                type="phrase_prefix",
                slop=2,
            )
            self.search_obj = self.search_obj.query(query)

    def order(self, order_by="-date_published"):
        """Sort results by the given field"""
        self.search_obj = self.search_obj.sort(order_by)

    def filter(
        self,
        topics=None,
        categories=None,
        language=None,
        to_date=None,
        from_date=None,
        archived=None,
    ):

        if topics is None:
            topics = []
        if categories is None:
            categories = []
        if language is None:
            language = []

        """Filter the results based on the given keyword arguments"""
        self.filter_topics(topics=topics)
        self.filter_categories(categories=categories)
        self.filter_language(language=language)
        self.filter_date(from_date=from_date, to_date=to_date)
        self.filter_archived(archived=archived)

    def search(self, title="", order_by="date_published"):
        """Perform a search for the given title"""
        self.search_title(title=title)
        self.order(order_by=order_by)
        return self.search_obj[0 : self.count()].to_queryset()

    def count(self):
        """Return the search object's current result count"""
        return self.search_obj.count()

    def get_raw_results(self, order_by="date_published"):
        """Get the Elasticsearch DSL Resposne object for current results.

        This can be called any time, before, between, or after calls to
        filter() or search().

        See the Elasticsearch DSL documentation for more on the Response
        object:
        https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#response
        """
        self.order(order_by=order_by)
        search = self.search_obj[0 : self.count()]

        # Also aggregate unique languages in the result.
        search.aggs.bucket("languages", A("terms", field="language"))

        return search.execute()


class EventFilterablePagesDocumentSearch(FilterablePagesDocumentSearch):
    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range", **{"start_dt": {"gte": from_date}}
            ).filter("range", **{"end_dt": {"lte": to_date}})

    def filter(self, **kwargs):
        self.search_obj = self.search_obj.filter(
            "term", model_class="EventPage"
        )
        super().filter(**kwargs)


class EnforcementActionFilterablePagesDocumentSearch(
    FilterablePagesDocumentSearch
):
    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range",
                **{"initial_filing_date": {"gte": from_date, "lte": to_date}},
            )

    def filter(self, statuses=None, products=None, **kwargs):
        if statuses is None:
            statuses = []
        if products is None:
            products = []

        self.search_obj = self.search_obj.filter(
            "term", model_class="EnforcementActionPage"
        )

        if statuses != []:
            self.search_obj = self.search_obj.filter(
                "terms", statuses=statuses
            )

        if products != []:
            self.search_obj = self.search_obj.filter(
                "terms", products=products
            )

        super().filter(**kwargs)

    def order(self, order_by="-initial_filing_date"):
        self.search_obj = self.search_obj.sort("-initial_filing_date")
