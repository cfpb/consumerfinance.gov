from django.core.exceptions import FieldDoesNotExist

from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from opensearchpy.helpers.query import MultiMatch

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
    model_class = fields.KeywordField()

    path = fields.KeywordField()
    depth = fields.IntegerField()
    title = fields.TextField(fields={"raw": fields.KeywordField()})
    live = fields.BooleanField()

    start_date = fields.DateField()
    end_date = fields.DateField()
    language = fields.KeywordField()

    tags = fields.ObjectField(
        properties={"slug": fields.KeywordField(), "name": fields.TextField()}
    )
    categories = fields.ObjectField(properties={"name": fields.KeywordField()})

    statuses = fields.KeywordField()
    products = fields.KeywordField()
    content = fields.TextField()

    def update(self, thing, *args, **kwargs):
        if isinstance(thing, AbstractFilterPage):
            thing = thing.specific

        return super().update(thing, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return AbstractFilterPage.objects.live().public().specific()

    def prepare_model_class(self, instance):
        return instance.__class__.__name__

    def prepare_start_date(self, instance):
        return getattr(instance, instance.__class__.start_date_field)

    def prepare_end_date(self, instance):
        if hasattr(instance.__class__, "end_date_field"):
            return getattr(instance, instance.__class__.end_date_field)
        else:
            return self.prepare_start_date(instance)

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
        auto_refresh = False


class FilterablePagesDocumentSearch:
    def __init__(self, root_page, children_only=True, ordering=None):
        search = FilterablePagesDocument.search()
        search = search.filter("prefix", path=root_page.path)
        search = search.filter("term", live=True)

        if children_only:
            search = search.filter("term", depth=root_page.depth + 1)
        else:
            search = search.filter("range", depth={"gt": root_page.depth})

        if ordering:
            search = search.sort(ordering)

        self.search_obj = search
        self._count = None

    def filter_topics(self, topics=None):
        if topics is None:
            topics = []
        if topics not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", tags__slug=topics
            )
            self._count = None

    def filter_categories(self, categories=None):
        if categories is None:
            categories = []
        if categories not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", categories__name=categories
            )
            self._count = None

    def filter_language(self, language=None):
        if language is None:
            language = []
        if language not in ([], "", None):
            self.search_obj = self.search_obj.filter(
                "terms", language=language
            )
            self._count = None

    def filter_date(self, from_date=None, to_date=None):
        if from_date and to_date:
            ranges = [
                {"end_date": {"gte": from_date}},
                {"start_date": {"lte": to_date}},
            ]
        elif from_date:
            ranges = [{"end_date": {"gte": from_date}}]
        elif to_date:
            ranges = [{"start_date": {"lte": to_date}}]
        else:
            ranges = []

        for range in ranges:
            self.search_obj = self.search_obj.filter("range", **range)

        if ranges:
            self._count = None

    def search_title(self, title=""):
        if title not in ([], "", None):
            query = MultiMatch(
                query=title,
                fields=[
                    "title^10",
                    "tags.name^10",
                    "content",
                ],
                type="phrase_prefix",
                slop=2,
            )
            self.search_obj = self.search_obj.query(query)
            self._count = None

    def filter(
        self,
        topics=None,
        categories=None,
        language=None,
        to_date=None,
        from_date=None,
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
        self._count = None

    def search(self, title=""):
        """Perform a search for the given title"""
        self.search_title(title=title)
        self._count = None
        return self.search_obj

    def count(self):
        """Return the search object's current result count"""
        if self._count is None:
            self._count = self.search_obj.count()
        return self._count

    def get_raw_results(self):
        """Get the Elasticsearch DSL Response object for current results.

        This can be called any time, before, between, or after calls to
        filter() or search().

        See the Elasticsearch DSL documentation for more on the Response
        object:
        https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#response
        """
        search = self.search_obj[0 : self.count()]

        # Aggregate unique languages in the result.
        search.aggs.bucket("languages", "terms", field="language")

        # Determine the earliest page date.
        search.aggs.metric("min_start_date", "min", field="start_date")

        return search.execute()


class EventFilterablePagesDocumentSearch(FilterablePagesDocumentSearch):
    def filter(self, **kwargs):
        self.search_obj = self.search_obj.filter(
            "term", model_class="EventPage"
        )
        super().filter(**kwargs)


class EnforcementActionFilterablePagesDocumentSearch(
    FilterablePagesDocumentSearch
):
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
