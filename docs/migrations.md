# Django and Wagtail Migrations

Adding or changing fields on Django models, Wagtail page models
(which are a particular kind of Django model), or StreamField block classes
will always require a new [Django schema migration](#schema-migrations);
additionally, changing field names or types on an existing block will require a
[Django data migration](#data-migrations).


## Table of contents

1. [Reference material](#reference-material)
1. [Do I need to create a migration?](#do-i-need-to-create-a-migration)
1. [Schema migrations](#schema-migrations)
1. [Data migrations](#data-migrations)
   1. [Wagtail-specific consideration](#wagtail-specific-considerations)
   1. [Utility functions](#utility-functions)
1. [Recreating migrations](#recreating-migrations)


## Reference material

The following links may be useful for setting context or diving deeper
into the concepts presented throughout this page:

- [Django migrations documentation](https://docs.djangoproject.com/en/1.11/topics/migrations/)
- [Django data migrations documentation](https://docs.djangoproject.com/en/1.11/topics/migrations/#data-migrations)
- [Wagtail Streamfield migrations documentation](https://docs.wagtail.io/en/stable/topics/streamfield.html#migrations)


## Do I need to create a migration?

A new Django migration is required for most, but not all, changes that you
make to the definitions of Django model classes. Even experienced Django
developers may find it unintuitive to determine which changes will require
a migration.

Example model changes that require a migration:

- Adding, removing, or renaming a model field
- Changing a model field definition in a way that impacts the database schema
(for example, changing the size of a `CharField`)
- Changing a model field definition in a way that does not impact the database schema
(for example, changing the field's `help_text`)

Example model changes that do not require a migration:

- Adding, removing, renaming, or modifying a model class method
- Modifying a model class [manager](https://docs.djangoproject.com/en/1.11/topics/db/managers/)

The best way to tell if your changes require a migration is to ask Django to
determine that for you. Django's
[makemigrations](https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-makemigrations)
management command can be used for this purpose:

```bash
./cfgov/manage.py makemigrations --dry-run
```

If you haven't made any changes to your local source code that would necessitate the
creation of a new migration, this command will print `No changes detected`.

Otherwise, if you have made changes that require a migration, Django will print
information about the migration that would need to be created:

```bash
Migrations for 'v1':
  cfgov/v1/migrations/0154_auto_20190412_1008.py
    - Alter field alt on cfgovimage
```

Running with the `--dry-run` flag won't actually create any migration files on disk.
See below for more information on how to do this, including how to give your
migrations a more descriptive name.


## Schema migrations

Any time you add or change a field on a Django model, Wagtail page model
(which are a particular kind of Django model), or StreamField block class, a
[Django schema migration](https://docs.djangoproject.com/en/1.11/topics/migrations)
will be required. This includes changes as small as modifying the `help_text` string.

To automatically generate a schema migration,
run the following, editing it to give your migration a name
that briefly describes the change(s) you're making:

```bash
./cfgov/manage.py makemigrations -n <description_of_changes>
```

For examples of good migration names, look through some of
[our existing migration files](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/v1/migrations).

!!! note
    Some changes will generate multiple migration files.
    If you change a block that is used in pages defined in different sub-apps,
    you will see a migration file for each of those sub-apps.

### Migration numbering and conflicts

When a migration file is generated, it will automatically be given
a unique four-digit number at the beginning of its filename.
These numbers are assigned in sequence, and they end up being
a regular source of conflicts between pull requests
that are in flight at the same time.
If a PR with a migration gets merged between the time you create your migration
and the time that your PR is ready for merging,
you will have to update your branch as normal to be current with main
and then re-create your migration.
Also note that our
[back-end tests that run in GitHub Actions](../github-actions/)
will fail if a required schema migration is missing or if
migrations are in conflict with one another.


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

!!! note
    While backwards migrations are necessary in external libraries that we create,
    we do not require them in consumerfinance.gov
    because we prefer not to rollback migrations that have already been applied.

### Wagtail-specific considerations

Django data migrations with Wagtail can be challenging because
[programmatic editing of Wagtail pages is difficult](https://github.com/wagtail/wagtail/issues/1101),
and pages have both revisions and StreamFields.
This section describes ways we try to address these challenges in consumerfinance.gov.

The data migration needs to modify both the existing Wagtail pages
that correspond to the changed model and all revisions of that page.
It also needs to be able to manipulate the contents of StreamFields.

As described in the
[editing a component guide](../editing-components/#editing-a-field),
it's a three-step process to modify a field without losing data:

1. Create the new field with an automatic schema migration
2. Use a handwritten data migration script to move data
   from the old field to the new field
3. Delete the old field with an automatic schema migration

We've written some utility functions in consumerfinance.gov
that make writing data migrations for StreamFields easier.
Using these utilities, a Django data migration that modifies a StreamField
would use the following format:

```python
from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields


def forward_mapper(page_or_revision, data):
    # Manipulate the stream block data forwards
    return data


def backward_mapper(page_or_revision, data):
    # Manipulate the stream block data backwards
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('myapp', 'MyPage', 'field_name', 'block_name'),
    ]
    migrate_page_types_and_fields(
        apps,
        page_types_and_fields,
        forward_mapper
    )


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('myapp', 'MyPage', 'field_name', 'block_name'),
    ]
    migrate_page_types_and_fields(
        apps,
        page_types_and_fields,
        backward_mapper
    )


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
```

`field_name` is the name of the StreamField on the Page model that contains the blocks to migrate.
`block_name` is the name of the block within a StreamField that contains the data to be migrated.

StreamBlocks can themselves also contain child blocks.
The block name can be given as a list of block names
that form the "path" to the block that needs to be migrated.
For example :

```python
def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('myapp', 'MyPage', 'field_name', ['parent_block', 'child_block']),
    ]
    migrate_page_types_and_fields(
        apps,
        page_types_and_fields,
        forward_mapper
    )
```

In this example,
a block with the name `child_block`
that is inside a block named `parent_block`
will be passed to the `forward_mapper` function.

The `data` that gets passed to the `forward_mapper` or `backward_mapper`
is a JSON-compatible Python `dict` that corresponds to the block's schema.

### Utility functions

These functions, defined in `v1.util.migrations`,
are used in the above data migration example.
They reduce the amount of boilerplate required
to work with Wagtail StreamField data in data migrations.

#### `migrate_page_types_and_fields(apps, page_types_and_fields, mapper)`

Migrate the fields of a Wagtail page type using the given `mapper` function.
`page_types_and_fields` should be a list of 4-tuples providing
`('app', 'PageType', 'field_name', 'block_name')` or
`('app', 'PageType', 'field_name', ['parent_block_name', 'child_block_name'])`.

`field_name` is the name of the StreamField on the Page model.

`block_name` is the name of the StreamBlock within the StreamField to migrate.

The mapper function should take `page_or_revision`
and the stream block's value as a `dict`.

This function calls `migrate_stream_field()`.

#### `migrate_stream_field(page_or_revision, field_name, block_path, mapper)`

Migrate all occurrences of the block name
contained within the `block_path` list
belonging to the page or revision using the `mapper` function.

The mapper function should take `page_or_revision`
and the stream block's value as a `dict`.

This function calls `migrate_data()`.

#### `migrate_data(page_or_revision, block_path, data, mapper)`

Migrate all occurrences of the block name
contained within the `block_path` list
within the `data` `dict`
using the given `mapper` function.

The mapper function should take `page_or_revision`
and the stream block's value as a `dict`.

#### `get_data(page_or_revision, field_name)`

Get the StreamField data for a given field name on a page or a revision.

This function will return a list of `dict`-like objects
containing the blocks within the given StreamField.

#### `set_data(page_or_revision, field_name, data, commit=True)`

Set the StreamField data for a given field name on a page or a revision.
If commit is `True` (default),
`save()` is called on the `page_or_revision` object.

`data` must be a list of `dict`-like objects
containing the blocks within the given StreamField.

## Recreating migrations

[As described above](#schema-migrations),
each time a Django model's definition changes it requires the generation of a new Django migration.
Over time, the number of migrations in our apps can grow very large,
slowing down testing and the `migrate` command.

For this reason it may be desirable to periodically delete and recreate the migration files,
so that instead of a series of files detailing every change over time
we have a smaller set that just describes the current state of models in the code.

Django does provide an automated
[squashing](https://docs.djangoproject.com/en/1.11/topics/migrations/#squashing-migrations)
process for migrations,
but this is often not optimal when migrations contain manual `RunPython` blocks that we don't necessarily care about keeping around.

Instead, we delete all existing migration files and then run `manage.py makemigrations` to create new ones.
This will generate the smallest number of migration files needed to describe the state of models in the code;
typically one per app although sometimes multiple are needed due to app dependencies.

This process does have these critical side effects:

1. Databases that exist at some migration state before the one at the point of the recreation will no longer be able to be migrated to the current state,
    as the intermediate changes will have been lost.
    This means that those databases will need to be recreated.
    This also means that historical database archives will require a bit more work to resurrect;
    they'll need to first be migrated to the point just before the recreation,
    and then updated to code at or after that point.

    For example, say a database dump exists at a point where N migrations occur.
    At such time as N + 1 migrations occur,
    we decide to go through the recreation process.
    Now we have a new migration numbered N + 2 that represents the equivalent of all (1..N+1) migrations that it replaces.
    If you try to load and migrate the dump at point N,
    Django no longer has the code necessary to go from N->N+1 only --
    it only has the ability to go from 0->N+2.
    To recover such a dump, you'll need to check out the code at the point before the recreation was done,
    migrate from N->N+1, and then check out latest and migrate forwards.

2. Any open pull requests at the time of the recreation that reference
    or depend on some of the existing migrations
    will need to be modified to instead refer to the new migration files.

Migrations can be recreated with this process:

1. Remove all existing migration files:

    ```sh
    rm -f -v cfgov/*/migrations/0*
    ```

2. Create new migration files from the state of model Python code:

    ```sh
    cfgov/manage.py makemigrations --noinput
    ```

    As it happens this creates new initial migrations (`0001_initial`) for all apps,
    plus some subsequent migrations (`0002_something`) for apps that depend on other apps
    (for example, `ask_cfpb` has its own initial migration and then some changes that rely on `v1`).

3. Rename the created migration files so that they follow in sequence the migration files that used to exist.
   For example, if at the time of recreation there are 101 `v1` migrations,
   the first new migration should be numbered 102.

4. Manually alter all new migration files to indicate that they replace the old migration files.

    This involves adding lines to these files like:

    ```py
    replaces = [('app_name', '0002_foo'), ('app_name', '0003_bar'), ...]
    ```

    This tells Django that these new files replace the old files,
    so that when migrations are run again,
    it doesn't need to do anything.

    Also manually update any new subsequent migration files so that they properly refer to each other.
    For example, if an app has two new migrations 102 and 103,
    the 103 file needs to properly depend on 102.

To apply these new migration files to an existing database, you can simply run:

```sh
cfgov/manage.py migrate --noinput
```

You'll see that there are no changes to apply,
as the new files should exactly describe the current model state in the same way that the old migrations did.

See [consumerfinance.gov#3770](https://github.com/cfpb/consumerfinance.gov/pull/3770) for an example of when this was done.
