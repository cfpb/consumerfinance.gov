# Django and Wagtail Migrations

Adding or changing fields on Django models, Wagtail page models
(which are a particular kind of Django model), or StreamField block classes
will always require a new [Django schema migration](#schema-migrations);
additionally, changing field names or types on an existing block will require a
[Django data migration](#data-migrations).


## Table of contents

1. [Reference material](#reference-material)
1. [Schema migrations](#schema-migrations)
1. [Data migrations](#data-migrations)
   1. [Wagtail-specific consideration](#wagtail-specific considerations)
   1. [Utility functions](#utility-functions)


## Reference material

The following links may be useful for setting context or diving deeper
into the concepts presented throughout this page:

- [Django migrations documentation](https://docs.djangoproject.com/en/1.11/topics/migrations/)
- [Django data migrations documentation](https://docs.djangoproject.com/en/1.11/topics/migrations/#data-migrations)
- [Wagtail Streamfield migrations documentation](https://docs.wagtail.io/en/v1.13.4/topics/streamfield.html#migrations)


## Schema migrations

Any time you add or change a field on a Django model, Wagtail page model
(which are a particular kind of Django model), or StreamField block classes, a
[Django schema migration](https://docs.djangoproject.com/en/1.11/topics/migrations)
will be required.

To automatically generate a schema migration,
run the following, editing it to give your migration a name
that briefly describes the change(s) you're making:

```bash
./cfgov/manage.py makemigrations -n <description_of_changes>
```

Be aware that each migration must have
a unique four-digit number at the beginning of its filename,
which is a regular source of conflicts between pull requests
that are in flight at the same time.
If a PR with a migration gets merged between the time you create your migration
and the time that your PR is ready for merging,
you will have to update your branch as normal to be current with master
and then re-create your migration.
Also note that our [back-end tests that run in Travis](../travis/)
will fail if a required schema migration is missing or if
migrations are in conflict with one another.

!!! note
    Some changes will generate multiple migration files.
    If you change a block that is used in pages defined in different sub-apps,
    you will see a migration file for each of those sub-apps.


## Data migrations

[Data migrations](https://docs.djangoproject.com/en/1.11/topics/migrations/#data-migrations)
are required any time you:

- rename an existing field
- change the type of an existing field
- delete an existing field
- rename a block within a StreamField
- delete a block

if you do not want to lose any data already stored in that field or block.

In other words, if an existing field or block is changing,
any data stored in that field or block has to be migrated to a different place,
unless you're OK with jettisoning it.

There is no automatic generation mechanism like there is for schema migrations.
You must write the script by hand that automates the transfer of data
from old fields to new fields.

To generate an empty migration file for your data migration, run:

```bash
./cfgov/manage.py makemigrations --empty yourappname
```

You can also copy the code below to get started with
`forward()` and `backward()` functions to migrate your model's data:

```python
from django.db import migrations


def forwards(apps, schema_editor):
    MyModel = apps.get_model('yourappname', 'MyModel')
    for obj in MyModel.objects.all():
        # Make forward changes to the object
        pass


def backwards(apps, schema_editor):
    MyModel = apps.get_model('yourappname', 'MyModel')
    for obj in MyModel.objects.all():
        # Make backward changes to the object
        pass


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
```

The `forwards()` and `backwards()` functions are where any changes
that need to happen to a model's data are made.


### Wagtail-specific considerations

Django data migrations with Wagtail can be challenging because
[programmatic editing of Wagtail pages is difficult](https://github.com/wagtail/wagtail/issues/1101),
and pages have both revisions and StreamFields.
This section describes ways we try to address these challenges in cfgov-refresh.

The data migration needs to modify both the existing Wagtail pages
that correspond to the changed model and all revisions of that page.
It also needs to be able to manipulate the StreamField contents.


As described in the
[editing a component guide](../editing-components/#editing-a-field),
it's a three-step process to modify a field without losing data:

1. Create the new field with an automatic schema migration
2. Use a handwritten data migration script to move data
   from the old field to the new field
3. Delete the old field with an automatic schema migration

We've written some utility functions in cfgov-refresh
that make writing data migrations for StreamFields easier.
Using these utilities, a Django data migration that modifies a StreamField
would use the following format:

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

These functions, defined in `v1.util.migrations`,
are used in the above data migration example.

#### `migrate_page_types_and_fields(apps, page_types_and_fields, mapper)`

Migrate the fields of a Wagtail page type using the given mapper function.
`page_types_and_fields` should be a list of 4-tuples providing
`('app', 'PageType', 'field_name', 'block type')`.

The mapper function should take `page_or_revision` and the stream block value.

#### `migrate_stream_field(page_or_revision, field_name, block_type, mapper)`

Migrate a block of the type within a StreamField of the name
belonging to the page or revision using the mapper function.

The mapper function should take `page_or_revision` and the stream block value.

#### `get_stream_data(page_or_revision, field_name)`

Get the StreamField data for a given field name on a page or a revision.

This function will return a list of `dict`-like objects
containing the blocks within the given StreamField.

#### `set_stream_data(page_or_revision, field_name, stream_data, commit=True)`

Set the StreamField data for a given field name on a page or a revision.
If commit is `True` (default),
`save()` is called on the `page_or_revision` object.

`stream_data` must be a list of `dict`-like objects
containing the blocks within the given StreamField.
