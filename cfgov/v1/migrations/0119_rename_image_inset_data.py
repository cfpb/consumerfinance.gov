from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields


def forward_mapper(page_or_revision, data):
    for field in data:
        if field['type'] == 'image_inset':
            field.update({
                'type': 'image',
            })

    return data


def backward_mapper(page_or_revision, data):
    for field in data:
        if field['type'] == 'image':
            field.update({
                'type': 'image_inset',
            })

    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('regulations3k', 'RegulationPage', 'content', 'full_width_text'),
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


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('regulations3k', 'RegulationPage', 'content', 'full_width_text'),
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
                                  backward_mapper)


class Migration(migrations.Migration):
    dependencies = [
        ('regulations3k', '0013_add_image_to_fullwidthtext'),
        ('v1', '0118_add_image_to_fullwidthtext')
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
