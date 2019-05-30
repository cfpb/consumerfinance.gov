from __future__ import unicode_literals

from django.utils.html import strip_tags
from haystack import indexes

import unidecode

from ask_cfpb.models.pages import AnswerPage
from search import fields


class AnswerPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharFieldWithSynonyms(
        document=True,
        use_template=True,
        boost=10.0)
    answer_text = indexes.CharField()
    answer_unaccented = indexes.CharField()
    autocomplete = indexes.EdgeNgramField(
        use_template=True)
    url = indexes.CharField(
        use_template=True,
        indexed=False)
    tags = indexes.MultiValueField(
        boost=10.0)
    language = indexes.CharField(
        model_attr='language')
    portal_topics = indexes.MultiValueField()
    portal_categories = indexes.MultiValueField()
    suggestions = indexes.FacetCharField()

    def prepare_tags(self, obj):
        return obj.clean_search_tags

    def prepare_portal_topics(self, obj):
        return [topic.heading for topic in obj.portal_topic.all()]

    def prepare_portal_categories(self, obj):
        return [topic.heading for topic in obj.portal_category.all()]

    def extract_raw_text(self, stream_data):
        # We want answer text to come first, to show up in result snippets.
        text_chunks = [
            block.get('value').get('content')
            for block in stream_data
            if block.get('type') == 'text'
        ]
        extra_chunks = [
            block.get('value').get('content')
            for block in stream_data
            if block.get('type') in ['tip', 'table']
        ]
        chunks = text_chunks + extra_chunks
        return " ".join(chunks)

    def prepare_answer_text(self, obj):
        stream = obj.answer_content
        raw_text = self.extract_raw_text(stream.stream_data)
        return strip_tags(raw_text)

    def prepare_answer_unaccented(self, obj):
        text = ''
        if obj.language == 'en':
            return text
        stream = obj.answer_content
        raw_text = self.extract_raw_text(stream.stream_data)
        stripped = strip_tags(raw_text)
        try:
            text = unidecode.unidecode(stripped)
        except Exception:
            pass
        return text

    def prepare(self, obj):
        data = super(AnswerPageIndex, self).prepare(obj)
        data['suggestions'] = data['text']
        return data

    def get_model(self):
        return AnswerPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            live=True, redirect_to_page=None)
