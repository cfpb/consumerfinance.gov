from haystack import indexes

from ask_cfpb.models.pages import AnswerPage
from search import fields


class AnswerBaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharFieldWithSynonyms(
        document=True,
        use_template=True,
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        use_template=True,
        indexed=True)
    url = indexes.CharField(
        use_template=True,
        indexed=False)
    tags = indexes.MultiValueField(
        indexed=True,
        boost=10.0)
    language = indexes.CharField(
        model_attr='language')
    suggestions = indexes.FacetCharField()

    def prepare_answer(self, obj):
        data = super(AnswerBaseIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def prepare_tags(self, obj):
        return obj.clean_search_tags

    def prepare(self, obj):
        data = super(AnswerBaseIndex, self).prepare(obj)
        data['suggestions'] = data['text']
        return data

    def get_model(self):
        return AnswerPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            live=True, redirect_to_page=None)
