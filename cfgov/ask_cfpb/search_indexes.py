from haystack import indexes

from ask_cfpb.models import Answer

# SEARCH_ASPECTS = [
#     ('most relevant', '-score'),
#     # ('most helpful', '-helpfulness_score'),
#     # ('most viewed', '-views'),
#     ('recently updated', '-updated_at'),

# ]


class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        use_template=True, indexed=True, stored=True)
    spanish = indexes.CharField(
        use_template=True,
        boost=10.0,
        indexed=True,
        stored=True)
    spanish_autocomplete = indexes.EdgeNgramField(
        use_template=True, indexed=True, stored=True)
    category = indexes.MultiValueField(
        indexed=True,
        stored=True,
        faceted=True,
        model_attr='category_text',
        boost=10.0)
    subcategory = indexes.MultiValueField(
        indexed=True,
        stored=True,
        faceted=True,
        model_attr='subcat_slugs',
        boost=10.0)
    tag = indexes.MultiValueField(
        indexed=True,
        stored=True,
        model_attr='tags',
        faceted=True,
        boost=10.0)
    audience = indexes.MultiValueField(
        indexed=True,
        stored=True,
        model_attr='audience_strings',
        faceted=True)
    created_at = indexes.DateTimeField(
        indexed=True, stored=True, model_attr='created_at')
    updated_at = indexes.DateTimeField(
        indexed=True, stored=True, model_attr='updated_at')
    # helpfulness_score = indexes.IntegerField(
    #     indexed=True, stored=True, model_attr='answer__helpfulness_score')
    # views = indexes.IntegerField(
    #     indexed=True, stored=True, model_attr="answer__viewcount")
    # boost = indexes.FloatField(model_attr='boost')

    def prepare(self, obj):
        data = super(AnswerIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    # def should_update(self, instance, **kwargs):
    #     return instance.workflow_state == 'APPROVED'

    def get_model(self):
        return Answer

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(workflow_state='APPROVED')
