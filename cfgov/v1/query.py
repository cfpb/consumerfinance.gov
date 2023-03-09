from django.db.models.expressions import RawSQL

from wagtail.fields import StreamField
from wagtail.query import PageQuerySet


class StreamBlockPageQuerySet(PageQuerySet):
    """Enable filtering and annotation on blocks in StreamFields on Pages.

    This class uses PostgreSQL’s built-in JSON support to create a temporary
    table of blocks within a specific `StreamField`, and the uses that table
    to filter a query for a specific target block within that `StreamField` or
    to annotate a query with the value of the ***first*** of any target blocks.

    For example:

    >>> from v1.models import CFGOVPage
    >>> from v1.query import StreamBlockPageQuerySet
    >>> qs = StreamBlockPageQuerySet(CFGOVPage).block_in_field(
    ...     "related_links", "sidefoot"
    ... ).annotate_block_in(
    ...     "related_links", "sidefoot"
    ... )
    >>> qs.first().related_links_value

    `block_in_field(target_block, streamfield_name)` will filter the queryset
    for any pages that contain the `target_block` name within a `StreamField`
    with the `streamfield_name`.

    `annotate_block_in(target_block, streamfield_name)` will annotate the query
    results with the JSON value of the first matching `target_block` within a
    `StreamField` with the `streamfield_name`.

    If a `StreamField` with the given `streamfield_name` does not exist, a
    `FieldDoesNotExist` exception wil be raised.

    If a field with the given `streamfield_name` exists, but is not a
    `StreamField`, a `TypeError` will be raised.
    """

    def _temp_block_table_sql_for_streamfield(self, streamfield_name):
        # Ensure the given streamfield_name is a StreamField on this queryset's
        # model.
        self._check_field(streamfield_name)

        # The following SQL will construct a temporary table intended to be
        # used as part of a larger query that will contain the page id,
        # block index, and block JSON object for each block within the JSON
        # array contained within the given StreamField. This uses PostgreSQL's
        # native JSON support for this construction.
        #
        # Note: this uses .format() instead of params to pass in the database
        # database_table, primary_key_field, and streamfield_name, because the
        # values for database_table and primary_key_field come from the model
        # attached to this QuerySet object itself, and the streamfield_name is
        # validated via the _check_field() method.
        #
        # Passing them through params creates quote formatting that doesn't
        # work with this query.
        return """
            WITH RECURSIVE blocks AS (
                SELECT page_id, index::text, block FROM (
                    SELECT
                        {primary_key_field} AS page_id,
                        {streamfield_name}::jsonb AS data FROM {database_table}
                ) x
                LEFT JOIN LATERAL jsonb_array_elements(x.data)
                WITH ORDINALITY AS a (block, index)
                ON true
                UNION ALL
                SELECT
                    page_id,
                    index || '.' || COALESCE(obj_key, (arr_key - 1)::text),
                    COALESCE(arr_block, obj_block)
                FROM blocks
                LEFT JOIN LATERAL
                    jsonb_array_elements(
                        CASE jsonb_typeof(block)
                            WHEN 'array' THEN block
                        END
                    )
                    WITH ORDINALITY as a(arr_block, arr_key)
                    ON jsonb_typeof(block) = 'array'
                LEFT JOIN LATERAL
                    jsonb_each(
                        CASE jsonb_typeof(block)
                            WHEN 'object' THEN block
                        END
                    )
                    AS o(obj_key, obj_block)
                    ON jsonb_typeof(block) = 'object'
                WHERE arr_key IS NOT NULL OR obj_key IS NOT NULL
            )
        """.strip().format(
            database_table=self.model._meta.db_table,
            primary_key_field=self.model._meta.pk.column,
            streamfield_name=streamfield_name,
        )

    def _check_field(self, streamfield_name):
        # This will raise a FieldDoesNotExist if a field with the given name
        # doesn't exist on the model.
        field = self.model._meta.get_field(streamfield_name)

        # If it's not a StreamField, raise a TypeError
        if not isinstance(field, StreamField):
            raise TypeError(f"{streamfield_name} is not a StreamField")

    def block_in_field(self, target_block, streamfield_name):
        """Filter the query for any target_block in streamfield_name"""
        base_sql = self._temp_block_table_sql_for_streamfield(streamfield_name)
        filter_sql = (
            base_sql
            + """
            SELECT
                page_id as {primary_key_field}
            FROM blocks
            WHERE block ->> 'type' = %s
        """.strip().format(
                primary_key_field=self.model._meta.pk.column,
            )
        )
        # Bandit will flag any use of RawSQL, thus the nosec on the next line.
        # target_block is passed as a parameter to RawSQL, adhering to Django's
        # documentation for avoiding SQL injection attacks.
        return self.filter(id__in=RawSQL(filter_sql, (target_block,)))  # nosec

    def annotate_block_in(self, target_block, streamfield_name):
        """Annotate the first target_block value's from streamfield_name"""
        base_sql = self._temp_block_table_sql_for_streamfield(streamfield_name)
        annotation_sql = (
            base_sql
            + """
            SELECT
                block ->> 'value'
            FROM blocks
            WHERE block ->> 'type' = %s
            LIMIT 1
        """.strip()
        )
        # Bandit will flag any use of RawSQL, thus the nosec in this return.
        # target_block is passed as a parameter to RawSQL, adhering to Django's
        # documentation for avoiding SQL injection attacks.
        return self.annotate(
            **{
                f"{target_block}_value": RawSQL(  # nosec
                    annotation_sql, (target_block,)
                )
            }
        )
