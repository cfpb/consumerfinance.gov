from haystack import indexes

from ask_cfpb.models.django import Answer


class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        boost=10.0)
    text_es = indexes.CharField(
        use_template=True,
        boost=10.0)
    english_autocomplete = indexes.EdgeNgramField(model_attr='question')
    spanish_autocomplete = indexes.EdgeNgramField(model_attr='question_es')
    category = indexes.MultiValueField(
        indexed=True,
        faceted=True,
        model_attr='category_text',
        boost=10.0)
    subcategory = indexes.MultiValueField(
        indexed=True,
        faceted=True,
        model_attr='subcat_slugs',
        boost=10.0)
    tag = indexes.MultiValueField(
        indexed=True,
        model_attr='tags',
        faceted=True,
        boost=10.0)
    audience = indexes.MultiValueField(
        indexed=True,
        model_attr='audience_strings',
        faceted=True)
    created_at = indexes.DateTimeField(
        indexed=True, model_attr='created_at')
    updated_at = indexes.DateTimeField(
        indexed=True, model_attr='updated_at')
    last_edited = indexes.DateTimeField(
        indexed=True, null=True, model_attr='last_edited')
    last_edited_es = indexes.DateTimeField(
        indexed=True, null=True, model_attr='last_edited_es')

    def prepare(self, obj):
        data = super(AnswerIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def get_model(self):
        return Answer

    def index_queryset(self, using=None):
        ids = [record.id for record in self.get_model().objects.all()
               if record.has_live_page()]
        return self.get_model().objects.filter(id__in=ids)
