from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from ask_cfpb.models.answer_page import AnswerPage
from search.elasticsearch_helpers import (
    environment_specific_index,
    ngram_tokenizer,
    synonym_analyzer,
)


@registry.register_document
class AnswerPageDocument(Document):

    autocomplete = fields.TextField(analyzer=ngram_tokenizer)
    portal_topics = fields.KeywordField()
    portal_categories = fields.TextField()
    text = fields.TextField(attr="text", analyzer=synonym_analyzer)
    url = fields.TextField()
    preview = fields.TextField(attr="answer_content_preview")

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
        name = environment_specific_index("ask-cfpb")
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = AnswerPage

        fields = [
            "search_tags",
            "language",
        ]
