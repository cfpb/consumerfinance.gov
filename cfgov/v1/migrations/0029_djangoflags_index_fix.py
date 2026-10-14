from django.db import migrations

# This is a one-off fix to convert an existing unique index on a
# django-flags table into a unique constraint. This is needed due to
# https://github.com/cfpb/django-flags/commit/10e690935ad4692129559f52652e65f3ba6e5ebe.
#
# https://github.com/cfpb/django-flags/blob/10e690935ad4692129559f52652e65f3ba6e5ebe/flags/models.py#L12-L16
table_name = "flags_flagstate"


index_name = "idx_16728_flags_flagstate_name_1d90a1cb81205552_uniq"


sql_template = """
DO $$ BEGIN
    IF EXISTS (SELECT FROM pg_indexes WHERE indexname='{index_name}') THEN
        DROP INDEX {index_name};
        ALTER TABLE {table_name} ADD CONSTRAINT {index_name} UNIQUE(name, condition, value);
    END IF;
END $$;
""".strip()


# Skip SQL if this is being run against a non-PostgreSQL database.
def fix_index(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        sql = sql_template.format(index_name=index_name, table_name=table_name)
        schema_editor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [
        ("v1", "0028_cfgovimage_description"),
    ]

    run_before = [
        ("flags", "0014_flagstate_unique_constraint"),
    ]

    operations = [
        migrations.RunPython(
            fix_index, migrations.RunPython.noop, elidable=True,
        )
    ]
