from django.urls import reverse

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from paying_for_college.models import School
from search.elasticsearch_helpers import (
    environment_specific_index, ngram_tokenizer
)


@registry.register_document
class SchoolDocument(Document):

    autocomplete = fields.TextField(analyzer=ngram_tokenizer)
    text = fields.TextField(attr='primary_alias', boost=10)
    url = fields.TextField()
    nicknames = fields.TextField()

    def get_queryset(self):
        """Prevent schools that have closed from being indexed."""
        query_set = super().get_queryset()
        return query_set.filter(operating=True)

    def prepare_autocomplete(self, instance):
        alias_strings = [a.alias for a in instance.alias_set.all()]
        nickname_strings = [n.nickname for n in instance.nickname_set.all()]
        auto_strings = alias_strings + nickname_strings + [str(instance.pk)]
        return " ".join(auto_strings)

    def prepare_nicknames(self, instance):
        return ", ".join([n.nickname for n in instance.nickname_set.all()])

    def prepare_url(self, instance):
        return reverse("paying_for_college:disclosures:school-json",
                       args=[instance.school_id])

    class Index:
        name = environment_specific_index('paying-for-college')
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
