from __future__ import unicode_literals

from haystack import indexes

from regulations3k.models import Section


class RegulationSectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True)
    title = indexes.CharField(model_attr='title')
    part = indexes.CharField(model_attr='subpart__version__part__part_number')
    date = indexes.DateField(model_attr='subpart__version__effective_date')

    def prepare_part(self, obj):
        return obj.subpart.version.part.__str__()

    def get_model(self):
        return Section

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(subpart__version__draft=False)
