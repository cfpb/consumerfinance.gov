from haystack import indexes

from college.models import School


class SchoolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='primary_alias')
    school_id = indexes.IntegerField(model_attr='school_id')
    nicknames = indexes.CharField()
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    autocomplete = indexes.EdgeNgramField()

    def get_model(self):
        return School

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(operating=True)

    def prepare_nicknames(self, obj):
        return obj.nicknames

    def prepare_autocomplete(self, obj):
        alias_strings = [a.alias for a in obj.alias_set.all()]
        nickname_strings = [n.nickname for n in obj.nickname_set.all()]
        auto_strings = alias_strings + nickname_strings
        auto_strings.append(str(obj.pk))
        return ' '.join(auto_strings)
