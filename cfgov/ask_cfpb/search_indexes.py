from haystack import indexes

from ask_cfpb.models.pages import AnswerPage
from search import fields


class AnswerPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharFieldWithSynonyms(
        document=True,
        use_template=True,
        boost=10.0)
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

    def prepare_answer(self, obj):
        data = super(AnswerPageIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def prepare_tags(self, obj):
        return obj.clean_search_tags

    def prepare_portal_topics(self, obj):
        return [topic.heading for topic in obj.portal_topic.all()]

    def prepare_portal_categories(self, obj):
        return [topic.heading for topic in obj.portal_category.all()]

    def prepare(self, obj):
        data = super(AnswerPageIndex, self).prepare(obj)
        data['suggestions'] = data['text']
        return data

    def get_model(self):
        return AnswerPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            live=True, redirect_to_page=None)
