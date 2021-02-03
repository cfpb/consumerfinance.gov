import sys

from django.db.models.lookups import Lookup

from wagtail.core.models import Page
from wagtail.search import index

from search.index import RelatedFilterField


# Elasticsearch 7 may be installed as 'elasticsearch7', but Wagtail's ES code
# assume that it is installed as 'elasticsearch'. Temporarily patch the import
# so that ES7 is imported from 'elasticsearch'.
elasticsearch = __import__('elasticsearch')
if elasticsearch.VERSION < (7,):
    sys.modules['elasticsearch'] = __import__('elasticsearch7')

 
from wagtail.search.backends.elasticsearch7 import (  # noqa: E402
    Elasticsearch7SearchBackend, Elasticsearch7SearchQueryCompiler
)


sys.modules['elasticsearch'] = elasticsearch


# https://docs.wagtail.io/en/v2.12/topics/search/indexing.html#index-relatedfields
class PageSearchQueryCompiler(Elasticsearch7SearchQueryCompiler):
    def _get_filterable_field(self, field_attname):
        field = super()._get_filterable_field(field_attname)

        if field:
            return field

        # We may be looking for a related field.
        related_fields = [
            field for field in self.queryset.model.get_search_fields()
            if isinstance(field, RelatedFilterField)
        ]

        for related_field in related_fields:
            if field_attname == '__'.join([
                related_field.field_name,
                related_field.related_field_name
            ]):
                return related_field

        return None

    def _get_filters_from_where_node(self, where_node, check_only=False):
        if isinstance(where_node, Lookup):
            field_attname = where_node.lhs.target.attname

            if not issubclass(
                self.queryset.model,
                where_node.lhs.target.model
            ):
                join = self.queryset.query.alias_map[where_node.lhs.alias]
                join_field_name = join.join_field.name
                field_attname = join_field_name + '__' + field_attname

                lookup = where_node.lookup_name
                value = where_node.rhs

                return self._process_filter(
                    field_attname,
                    lookup,
                    value,
                    check_only=check_only
                )

        return super()._get_filters_from_where_node(
            where_node,
            check_only=check_only
        )


class PageSearchBackend(Elasticsearch7SearchBackend):
    query_compiler_class = PageSearchQueryCompiler

    def get_index_for_model(self, model):
        if issubclass(model, Page):
            return super().get_index_for_model(model)


SearchBackend = PageSearchBackend
