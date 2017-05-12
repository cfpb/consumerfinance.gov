from haystack import indexes

from ask_cfpb.models.django import (
    EnglishAnswerProxy, SpanishAnswerProxy)

VALID_SPANISH_TAGS = SpanishAnswerProxy.valid_spanish_tags()


class AnswerBaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
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
    last_edited = indexes.DateTimeField(
        indexed=True,
        null=True,
        model_attr='last_edited',
        boost=2.0)

    def prepare_tags(self, obj):
        return obj.tags

    def prepare_answer(self, obj):
        data = super(AnswerBaseIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def get_model(self):
        return EnglishAnswerProxy

    def index_queryset(self, using=None):
        ids = [record.id for record in self.get_model().objects.all()
               if record.english_page and record.english_page.live is True]
        return self.get_model().objects.filter(id__in=ids)


class SpanishBaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
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
    last_edited = indexes.DateTimeField(
        indexed=True,
        null=True,
        model_attr='last_edited_es',
        boost=2.0)

    def prepare_tags(self, obj):
        return obj.tags_es

    def prepare_spanish_answer_index(self, obj):
        data = super(SpanishBaseIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def get_model(self):
        return SpanishAnswerProxy

    def index_queryset(self, using=None):
        ids = [record.id for record in self.get_model().objects.all()
               if record.spanish_page and record.spanish_page.live is True]
        return self.get_model().objects.filter(id__in=ids)
