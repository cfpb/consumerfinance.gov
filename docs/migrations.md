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
1. [Squashing migrations](#squashing-migrations)

## Reference material

The following links may be useful for setting context or diving deeper
into the concepts presented throughout this page:

- [Django migrations documentation](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django data migrations documentation](https://docs.djangoproject.com/en/stable/topics/migrations/#data-migrations)
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
- Modifying a model class [manager](https://docs.djangoproject.com/en/stable/topics/db/managers/)

The best way to tell if your changes require a migration is to ask Django to
determine that for you. Django's
[makemigrations](https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-makemigrations)
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
[Django schema migration](https://docs.djangoproject.com/en/stable/topics/migrations)
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
[back-end tests that run in GitHub Actions](github-actions.md)
will fail if a required schema migration is missing or if
migrations are in conflict with one another.

## Data migrations

[Data migrations](https://docs.djangoproject.com/en/stable/topics/migrations/#data-migrations)
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

Helpfully, Wagtail includes some utility functions that make it easier to
write StreamField data migrations. These are described in detail
[in the Wagtail documentation](https://docs.wagtail.org/en/stable/advanced_topics/streamfield_migrations.html#streamfield-data-migrations).

## Squashing migrations

[As described above](#schema-migrations),
each time a Django model's definition changes it requires the generation of a new Django migration.
Over time, the number of migrations in our apps can grow very large,
slowing down testing and the `migrate` command.

For this reason it may be desirable to periodically delete and recreate the migration files,
so that instead of a series of files detailing every change over time
we have a smaller set that just describes the current state of models in the code.

Django provides an automated
[squashing](https://docs.djangoproject.com/en/stable/topics/migrations/#squashing-migrations)
process for migrations, but this is often not optimal when migrations contain manual `RunPython` blocks are present.
Before running `squashmigrations`, search existing migrations for `RunPython` blocks without `elidable=True`, and
correct them to have `elidable=True`. This will tell `squashmigrations` to drop that `RunPython` block.
In almost _all_ cases, we do not want to keep any `RunPython` blocks.
It is highly recommended to get a postgres database setup with the current migrations before
attempting to squash.

1. Set all `RunPython` blocks to have the argument `elidable=True`.
2. Squash migrations for each app that has 3 or more non-squashed migrations

```sh
# start migration number is optional for apps that have never been squashed
cfgov/manage.py squashmigrations --squashed-name <year>_squash <app_name> <starting_migration_number> <ending_migration_number>

# 2022 ask_cfp squash 0039 -> 0045
cfgov/manage.py squashmigrations --squashed-name 2022_squash ask_cfpb 0039 0045

# 2022 form_explainer squash 0001 -> 0007
cfgov/manage.py squashmigrations --squashed-name 2022_squash form_explainer 0007
```

3. Once all apps are squashed, attempt to apply migrations to check for errors

```sh
cfgov/manage.py migrate
```

4. Correct errors, if any, until there are no migrations to apply or create.
   Repeat steps 3 and 4 until no errors.
   It may be possible that an additional migration will be generated
   if there was an error that needed to be corrected.

5. Unittest with squashed migrations in place
6. Recreate fresh database, and load `test.sql.gz`, and apply the migrations.

```sh
./refresh-data.sh test.sql.gz
```

8. Dump test database back to `test.sql.gz`

```sh
./dump-data.sh test.sql.gz
```

9. Delete non-squashed migration files that were squashed.

### Squash Notes

#### 2022

`teachers_digital_platform` had an over-optimization or circular dependency
issue, resulting in the following error.

```
ValueError: The field teachers_digital_platform.ActivityPage.student_characteristics was declared with a lazy reference to 'teachers_digital_platform.activityspecialpopulation', but app 'teachers_digital_platform' doesn't provide model 'activityspecialpopulation'.
The field teachers_digital_platform.ActivityPage_student_characteristics.activityspecialpopulation was declared with a lazy reference to 'teachers_digital_platform.activityspecialpopulation', but app 'teachers_digital_platform' doesn't provide model 'activityspecialpopulation'.
```

Corrected the error by changing the reference to the correct field for student char.
An additional migration was generated for `teachers_digital_platform` once this error was corrected.
`ActivitySpecialPopulation` -> `ActivityStudentCharacteristics`.
