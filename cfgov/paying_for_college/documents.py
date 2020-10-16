from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from paying_for_college.models import School
from search.elasticsearch_helpers import label_autocomplete


@registry.register_document
class SchoolDocument(Document):

    autocomplete = fields.TextField(analyzer=label_autocomplete)
    text = fields.TextField(attr='primary_alias', boost=10)
    nicknames = fields.TextField()

    def prepare_autocomplete(self, instance):
        alias_strings = [a.alias for a in instance.alias_set.all()]
        nickname_strings = [n.nickname for n in instance.nickname_set.all()]
        return alias_strings + nickname_strings

    def prepare_primary_alias(self, instance):
        return instance.primary_alias

    def prepare_nicknames(self, instance):
        return [n.nickname for n in instance.nickname_set.all()]

    class Index:
        name = 'paying-for-college'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = School

        fields = [
            'school_id',
            'city',
            'state',
            'zip5',
        ]
