from html import unescape

from django.core.exceptions import FieldDoesNotExist
from django.utils.html import strip_tags

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from flags.state import flag_enabled

from search.elasticsearch_helpers import environment_specific_index
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.learn_page import (
    AbstractFilterPage, DocumentDetailPage, EventPage, LearnPage
)
from v1.models.newsroom_page import LegacyNewsroomPage, NewsroomPage


@registry.register_document
class FilterablePagesDocument(Document):

    tags = fields.ObjectField(properties={
        'slug': fields.KeywordField(),
        'name': fields.TextField()
    })
    categories = fields.ObjectField(properties={
        'name': fields.KeywordField()
    })
    authors = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.KeywordField()
    })

    title = fields.TextField(attr='title')
    is_archived = fields.KeywordField(attr='is_archived')
    date_published = fields.DateField(attr='date_published')
    url = fields.KeywordField()
    start_dt = fields.DateField()
    end_dt = fields.DateField()
    statuses = fields.KeywordField()
    products = fields.KeywordField()
    initial_filing_date = fields.DateField()
    model_class = fields.KeywordField()
    content = fields.TextField()
    preview_description = fields.TextField()

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

    def prepare_content(self, instance):
        try:
            content_field = instance._meta.get_field('content')
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
            NewsroomPage
        ]

    class Index:
        name = environment_specific_index('filterable-pages')
        settings = {'index.max_ngram_diff': 23}


class FilterablePagesDocumentSearch:

    def __init__(self, prefix='/'):
        self.document = FilterablePagesDocument()
        self.search_obj = self.document.search().filter(
            'prefix', url=prefix
        )

    def filter_topics(self, topics=[]):
        if topics not in ([], '', None):
            self.search_obj = self.search_obj.filter(
                "terms",
                tags__slug=topics
            )

    def filter_categories(self, categories=[]):
        if categories not in ([], '', None):
            self.search_obj = self.search_obj.filter(
                "terms",
                categories__name=categories
            )

    def filter_authors(self, authors=[]):
        if authors not in ([], '', None):
            self.search_obj = self.search_obj.filter(
                "terms",
                authors__slug=authors
            )

    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range", **{
                    'date_published': {
                        'gte': from_date, 'lte': to_date
                    }
                }
            )

    def filter_archived(self, archived=None):
        if archived is not None:
            self.search_obj = self.search_obj.filter(
                "terms",
                is_archived=archived
            )

    def search_title(self, title=''):
        if title not in ([], '', None):
            if flag_enabled('EXPAND_FILTERABLE_LIST_SEARCH'):
                query = MultiMatch(
                    query=title,
                    fields=[
                        'title^10',
                        'tags.name^10',
                        'content',
                        'preview_description'
                    ],
                    type="phrase_prefix",
                    slop=2
                )
                self.search_obj = self.search_obj.query(query)
            else:
                self.search_obj = self.search_obj.query(
                    "match", title={"query": title, "operator": "AND"}
                )

    def order_results(self, title='', order_by='-date_published'):
        total_results = self.search_obj.count()
        # Marching on title is the only time we see an actual
        # impact on scoring, so we should only look to alter the order
        # if there is a title provided as part of the search.
        if not title:
            return self.search_obj.sort('-date_published')[0:total_results]
        else:
            return self.search_obj.sort(order_by)[0:total_results]

    def filter(self, topics=[], categories=[], authors=[], to_date=None,
               from_date=None, archived=None):
        self.filter_topics(topics=topics)
        self.filter_categories(categories=categories)
        self.filter_authors(authors=authors)
        self.filter_date(from_date=from_date, to_date=to_date)
        self.filter_archived(archived=archived)

    def search(self, title='', order_by='-date_published'):
        self.search_title(title=title)
        results = self.order_results(order_by=order_by)
        return results.to_queryset()


class EventFilterablePagesDocumentSearch(FilterablePagesDocumentSearch):
    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range", **{'start_dt': {'gte': from_date}}
            ).filter(
                "range", **{'end_dt': {'lte': to_date}}
            )

    def filter(self, **kwargs):
        self.search_obj = self.search_obj.filter(
            "term",
            model_class="EventPage"
        )
        super().filter(**kwargs)


class EnforcementActionFilterablePagesDocumentSearch(
    FilterablePagesDocumentSearch
):
    def filter_date(self, from_date=None, to_date=None):
        if to_date is not None and from_date is not None:
            self.search_obj = self.search_obj.filter(
                "range", **{
                    "initial_filing_date": {
                        "gte": from_date, "lte": to_date
                    }
                }
            )

    def filter(self, statuses=[], products=[], **kwargs):
        self.search_obj = self.search_obj.filter(
            "term",
            model_class="EnforcementActionPage"
        )

        if statuses != []:
            self.search_obj = self.search_obj.filter(
                "terms",
                statuses=statuses
            )

        if products != []:
            self.search_obj = self.search_obj.filter(
                "terms",
                products=products
            )

        super().filter(**kwargs)

    def order_results(self, order_by='-initial_filing_date'):
        total_results = self.search_obj.count()
        return self.search_obj.sort('-initial_filing_date')[0:total_results]
