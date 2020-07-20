# Based on https://wellfire.co/learn/custom-haystack-elasticsearch-backend/

from django.conf import settings
from haystack.backends.elasticsearch2_backend import (
    Elasticsearch2SearchBackend, Elasticsearch2SearchEngine
)


class CFGOVElasticsearch2SearchBackend(Elasticsearch2SearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(CFGOVElasticsearch2SearchBackend, self).__init__(
            connection_alias, **connection_options)

        custom_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        if custom_settings:
            setattr(self, 'DEFAULT_SETTINGS', custom_settings)

        custom_analyzer = getattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER')
        if custom_analyzer:
            setattr(self, 'DEFAULT_ANALYZER', custom_analyzer)

    def build_schema(self, fields):
        content_field_name, mapping = super(
            CFGOVElasticsearch2SearchBackend,
            self
        ).build_schema(fields)

        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]

            if field_mapping['type'] == 'string' and field_class.indexed:
                if (not hasattr(field_class, 'facet_for') and
                        field_class.field_type not in ('ngram', 'edge_ngram')):
                    field_mapping['analyzer'] = getattr(
                        field_class, 'analyzer', self.DEFAULT_ANALYZER)

            mapping.update({field_class.index_fieldname: field_mapping})

        return (content_field_name, mapping)


class CFGOVElasticsearch2SearchEngine(Elasticsearch2SearchEngine):
    backend = CFGOVElasticsearch2SearchBackend
