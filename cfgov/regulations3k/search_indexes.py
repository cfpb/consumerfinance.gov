
from haystack import indexes

from regulations3k.models import SectionParagraph


class RegulationParagraphIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True)
    title = indexes.CharField(model_attr='section__title')
    part = indexes.CharField(
        model_attr='section__subpart__version__part__part_number')
    date = indexes.DateField(
        model_attr='section__subpart__version__effective_date')
    section_order = indexes.CharField(model_attr='section__sortable_label')
    section_label = indexes.CharField(model_attr='section__label')
    paragraph_id = indexes.CharField(model_attr='paragraph_id')

    def get_model(self):
        return SectionParagraph

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
