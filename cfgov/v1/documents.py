from django.utils.html import strip_tags

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from html import unescape

from itertools import chain

import json

from v1.models.base import CFGOVAuthoredPages, CFGOVPageCategory, CFGOVTaggedPages
from v1.models.blog_page import BlogPage
from v1.models.learn_page import AbstractFilterPage, DocumentDetailPage, EventPage
from v1.models.enforcement_action_page import EnforcementActionPage

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
    title = fields.TextField(attr='title')
    is_archived = fields.TextField(attr='is_archived')
    content = fields.TextField()
    preview_description = fields.TextField()
    date_published = fields.DateField(attr='date_published')
    url = fields.KeywordField()
    specific_class = fields.TextField()
    start_dt = fields.DateField()
    statuses = fields.KeywordField()
    initial_filing_date = fields.DateField()
    related_metadata_tags = fields.TextField()

    def get_queryset(self):
        return AbstractFilterPage.objects.live().public()

    def prepare_content(self, instance):
        try:
            content_field = instance._meta.get_field('content')
            value = content_field.value_from_object(instance)
            content = content_field.get_searchable_content(value)
            # get_serachable_content returns a single-item list for a RichTextField
            # so we want to pop out the one item to just get a regular string
            content = content.pop()
            return content
        except:
            return None

    def prepare_preview_description(self, instance):
        return unescape(strip_tags(instance.preview_description))

    def prepare_url(self, instance):
        return instance.url

    def prepare_specific_class(self, instance):
        return instance.specific_class.__name__

    def prepare_start_dt(self, instance):
        try:
            return instance.specific.start_dt
        except:
            return None

    def prepare_statuses(self, instance):
        try:
            return [status.status for status in instance.specific.statuses.all()]
        except:
            return None

    def prepare_initial_filing_date(self, instance):
        try:
            return instance.specific.initial_filing_date
        except:
            return None
    
    def prepare_related_metadata_tags(self, instance):
        return json.dumps(instance.related_metadata_tags())

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, CFGOVAuthoredPages):
            return related_instance.authors.all()
        if isinstance(related_instance, CFGOVPageCategory):
            return related_instance.categories.all()
        if isinstance(related_instance, CFGOVTaggedPages):
            return related_instance.tags.all()

    class Django:
        model = AbstractFilterPage

        fields = [
            'secondary_link_url',
            'secondary_link_text',
            'preview_title',
            'preview_subheading',
            
        ]

        related_models = [
            CFGOVAuthoredPages,
            CFGOVPageCategory,
            CFGOVTaggedPages
        ]

    class Index:
        name = 'test'


class FilterablePagesDocumentSearch:
    
    def __init__(self, prefix='/', topics=[], categories=[], authors=[]):
         self.prefix = prefix
         self.topics = topics
         self.categories = categories
         self.authors = authors

    def search(self):
        search = FilterablePagesDocument.search()
        if self.prefix != '':
            search = search.filter('prefix', url=self.prefix)
        if self.topics not in ([], '', None):
            search = search.filter("terms", tags__slug=self.topics)
        if self.categories not in ([], '', None):
            search = search.filter("terms", categories__name=self.categories)
        if self.authors not in ([], '', None):
            search = search.filter("terms", authors__slug=self.authors)
            
        print(search.to_dict())
        total_results = search.count()
        results = search.sort('-date_published').execute()[0:total_results]
        print(results)
        return self.map_results(results)

    def map_results(self, results):
        return [
            {'title': hit.title, 'url': hit.url,
             'categories': hit.categories, 'tags': [{ 'slug': tag.slug } for tag in hit.tags], 
             'authors': [{'name': author.name, 'slug': author.slug } for author in hit.authors],
             'is_archived': hit.is_archived, 'specific_class': hit.specific_class,
             'start_dt': hit.start_dt, 'initial_filing_date': hit.initial_filing_date, 
             'date_published': hit.date_published,
             'related_metadata_tags': json.loads(hit.related_metadata_tags),
             'secondary_link_url': hit.secondary_link_url, 'secondary_link_text': hit.secondary_link_text,
             'preview_title': hit.preview_title, 'preview_subheading': hit.preview_subheading,
             'preview_description': hit.preview_description} for hit in results
        ]

    def set_topics(self, topics):
        self.search.filter("terms", tags__slug=topics)
        return self

    def set_categories(self, categories):
        self.search.filter("terms", categories__name=categories)
        return self

    def set_authors(self, authors):
        self.search.filter("terms", authors__slug=authors)
        return self

    def filter_queryset(self, path):
        self.search.filter("prefix", url=path)
        return self

    # Date Format needs to be YYYY-MM-DD
    def filter_date_published(self, from_date, to_date):
        return self.search.filter("range", **{'date_published': {'gte': from_date, 'lte': to_date}})

    def execute(self):
        total_results = self.search.count()
        return self.search.execute()[0:total_results]

