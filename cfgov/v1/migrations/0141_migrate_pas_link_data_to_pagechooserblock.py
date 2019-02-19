import re
from urlparse import urlparse

from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields
from v1.util.util import get_page_from_path


def forward_mapper(page_or_revision, data):
    old_disclaimer = data['form_field'][0]['info']
    page_id_link_pattern = re.compile(r'a id="(\d+)" linktype="page"')
    match = page_id_link_pattern.search(old_disclaimer)

    if match:
        page_id = int(match.group(1))
    else:
        href_link_pattern = re.compile(r'href="(.+)"')
        match = href_link_pattern.search(old_disclaimer)

        if match:
            path = urlparse(match.group(1)).path
            page = get_page_from_path(path)

            if page:
                page_id = page.pk
            else:
                page_id = 1189  # Generic Email Sign-Up Privacy Act Statement
        else:
            # Fall back on the Generic Email Sign-Up Privacy Act Statement
            page_id = 1189

    if page_id == 558 or page_id == 571:
        # Convert links to /privacy/privacy-policy/ and
        # /privacy/website-privacy-policy/ to the
        # Generic Email Sign-Up Privacy Act Statement
        page_id = 1189

    data['disclaimer_page'] = page_id

    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('ask_cfpb', 'AnswerPage', 'sidebar', 'email_signup'),
        (
            'regulations3k',
            'RegulationPage',
            'content',
            ['full_width_text', 'email_signup']
        ),
        (
            'regulations3k',
            'RegulationLandingPage',
            'content',
            ['full_width_text', 'email_signup']
        ),
        ('v1', 'CFGOVPage', 'sidefoot', 'email_signup'),
        ('v1', 'BlogPage', 'content', 'email_signup'),
        ('v1', 'BlogPage', 'content', ['full_width_text', 'email_signup']),
        ('v1', 'BrowsePage', 'content', ['full_width_text', 'email_signup']),
        (
            'v1',
            'BrowseFilterablePage',
            'content',
            ['full_width_text', 'email_signup']
        ),
        (
            'v1',
            'DocumentDetailPage',
            'content',
            ['full_width_text', 'email_signup']
        ),
        ('v1', 'LearnPage', 'content', 'email_signup'),
        ('v1', 'LearnPage', 'content', ['full_width_text', 'email_signup']),
        (
            'v1',
            'SublandingPage',
            'content',
            ['full_width_text', 'email_signup']
        ),
        (
            'v1',
            'SublandingFilterablePage',
            'content',
            ['full_width_text', 'email_signup']
        ),
    ]
    migrate_page_types_and_fields(apps,
                                  page_types_and_fields,
                                  forward_mapper)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0140_modify_emailsignup_organism')
    ]
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
