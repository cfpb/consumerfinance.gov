from django.db import migrations


def forwards(apps, schema_editor):
    # Set all is_archived fields to 'no' initially.
    CFGOVPage = apps.get_model('v1', 'CFGOVPage')
    all_pages = CFGOVPage.objects.all()

    for page in all_pages:
        page.is_archived = 'no'

    CFGOVPage.objects.bulk_update(all_pages, ['is_archived'])

def backwards(apps, schema_editor):
    # Set all is_archived fields back to 'false'.
    # (They had been cast from booleans to strings in 0233.)
    CFGOVPage = apps.get_model('v1', 'CFGOVPage')
    all_pages = CFGOVPage.objects.all()

    for page in all_pages:
        page.is_archived = 'false'

    CFGOVPage.objects.bulk_update(all_pages, ['is_archived'])


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0236_use_yes_no_for_string_choices'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
