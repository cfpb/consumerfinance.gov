from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from regulations3k.models import SectionParagraph
from search.elasticsearch_helpers import environment_specific_index


@registry.register_document
class SectionParagraphDocument(Document):

    text = fields.TextField(attr="paragraph", boost=10)
    title = fields.TextField()
    part = fields.KeywordField()
    date = fields.DateField()
    section_order = fields.KeywordField()
    section_label = fields.TextField()
    short_name = fields.TextField()

    def prepare_date(self, instance):
        return instance.section.subpart.version.effective_date

    def prepare_part(self, instance):
        return instance.section.subpart.version.part.part_number

    def prepare_section_label(self, instance):
        return instance.section.label

    def prepare_section_order(self, instance):
        return instance.section.sortable_label

    def prepare_short_name(self, instance):
        return instance.section.subpart.version.part.short_name

    def prepare_title(self, instance):
        return instance.section.title

    class Index:
        name = environment_specific_index("regulations3k")
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = SectionParagraph

        fields = ["paragraph_id"]
