from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields


def forward_mapper(page_or_revision, data):
    for field in data:
        if field['type'] == 'media':
            field.update({
                'type': 'image_inset',
                'value': {
                    'image': {
                        'upload': field['value']
                    },
                    'image_width': 'full',
                    'is_bottom_rule': False
                }
            })

    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'BlogPage', 'content', 'full_width_text'),
        ('v1', 'BrowseFilterablePage', 'content', 'full_width_text'),
        ('v1', 'BrowsePage', 'content', 'full_width_text'),
        ('v1', 'LearnPage', 'content', 'full_width_text'),
        ('v1', 'DocumentDetailPage', 'content', 'full_width_text'),
        ('v1', 'SublandingFilterablePage', 'content', 'full_width_text'),
        ('v1', 'SublandingPage', 'content', 'full_width_text'),
    ]
    migrate_page_types_and_fields(apps,
                                  page_types_and_fields,
                                  forward_mapper)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0116_single_wagtail_site')
    ]
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
