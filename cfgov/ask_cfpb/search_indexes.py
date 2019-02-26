from haystack import indexes

from ask_cfpb.models import Category
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
        ids = [record.id for record in self.get_model().objects.all()
               if record.live is True
               and record.redirect_to is None]
        return self.get_model().objects.filter(id__in=ids)


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True)
    facet_map = indexes.CharField(
        indexed=True)
    slug = indexes.CharField(
        model_attr='slug')
    slug_es = indexes.CharField(
        model_attr='slug_es')

    def prepare_facet_map(self, obj):
        return obj.facet_map

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


# class TagIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(
#         use_template=True,
#         document=True)

#     valid_spanish = indexes.MultiValueField()

#     def get_model(self):
#         return AnswerTagProxy

#     def prepare_valid_spanish(self, obj):
#         return self.get_model().valid_spanish_tags()

#     def index_queryset(self, using=None):
#         return self.get_model().objects.filter(id=1)
