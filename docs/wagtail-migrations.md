# Wagtail and Django data migrations

Django data migrations with Wagtail can be challenging because programmatic editing of Wagtail pages [is difficult](https://github.com/torchbox/wagtail/issues/1101), and pages have both revisions and StreamFields. This document is intended to describe ways we try to address these challenges in cfgov-refresh.

## Migrating StreamFields

StreamFields do not follow a fixed structure, rather they're a freeform sequences of blocks. Making a change to a StreamField involves both creating a [Django schema migration](https://docs.djangoproject.com/en/1.11/topics/migrations/#workflow) and a custom [Django data migration](https://docs.djangoproject.com/en/1.11/topics/migrations/#data-migrations). The data migration needs to modify both the existing Wagtail pages that correspond to the changed model and all revisions of that page. It also needs to be able to manipulate the StreamField contents.

To this end, there are some utility functions in cfgov-refresh that make this easier. Using these utilities, a Django data migration that modifies a StreamField would use the following format:

```python
from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields


def forward_mapper(page_or_revision, data):
    data = dict(data)
    # Manipulate the stream block data forwards
    return data


def backward_mapper(page_or_revision, data):
    data = dict(data)
    # Manipulate the stream block data backwards
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('myapp', 'MyPage', 'streamfield_name', 'streamblock_type'),
    ]
    migrate_page_types_and_fields(apps,
                                  page_types_and_fields,
                                  forward_mapper)


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('myapp', 'MyPage', 'streamfield_name', 'streamblock_type'),
    ]
    migrate_page_types_and_fields(apps,
                                  page_types_and_fields,
                                  backward_mapper)


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
```

### Utility functions

These functions are available in `v1.util.migrations`.

##### `migrate_page_types_and_fields(apps, page_types_and_fields, mapper)`

Migrate the fields of a wagtail page type using the given mapper function. page_types_and_fields should be a list of 4-tuples providing ('app', 'PageType', 'field_name', 'block type').

The mapper function should take `page_or_revision` and the stream block value.

##### `migrate_stream_field(page_or_revision, field_name, block_type, mapper)`

Migrate a block of the type within a StreamField of the name belonging to the page or revision using the mapper function.

The mapper function should take `page_or_revision` and the stream block value.

##### `get_stream_data(page_or_revision, field_name)`

Get the stream field data for a given field name on a page or a revision.

This function will return a list of `dict`-like objects containing the blocks within the given StreamField.

##### `set_stream_data(page_or_revision, field_name, stream_data, commit=True)`

Set the stream field data for a given field name on a page or a revision. If commit is True (default) `save()` is called on the `page_or_revision` object.

`stream_data` must be a list of `dict`-like objects containing the blocks within the given StreamField.
