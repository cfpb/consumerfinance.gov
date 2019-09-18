""" Data migration for EmailSignup Privacy Act statement links.

This data migration looks for the first link in the disclaimer RichTextBlock of
the first form_field in all EmailSignup blocks and converts that to the new
disclaimer_link PageChooserBlock on the EmailSignup.
"""

import re
from six.moves.urllib.parse import urlparse

from django.db import migrations

from v1.util.migrations import migrate_page_types_and_fields
from v1.util.util import get_page_from_path


def forward_mapper(page_or_revision, data):
    # Set the default disclaimer_page_id, which corresponds to
    # the Generic Email Sign-Up Privacy Act Statement.
    disclaimer_page_id = 1189
    data['disclaimer_page'] = disclaimer_page_id

    if not data.get('form_field'):
        return data
    elif not data['form_field'][0].get('info'):
        return data

    old_disclaimer = data['form_field'][0]['info']

    # First look to see if there is an internal Wagtail link in the field.
    page_id_link_pattern = re.compile(r'a id="(\d+)" linktype="page"')
    match = page_id_link_pattern.search(old_disclaimer)

    if match:
        # If there was a match for the internal link regex, set page_id to the
        # value of the link's id attribute.
        disclaimer_page_id = int(match.group(1))
    else:
        # If there was not an internal link, look for an "external" link (a
        # link where the path or full URL was entered by hand).
        href_link_pattern = re.compile(r'href="(.+)"')
        match = href_link_pattern.search(old_disclaimer)

        if match:
            # If there was a match for the internal link regex, get the page
            # that corresponds to the path and set disclaimer_page_id to its pk
            # value of the link's id attribute.
            path = urlparse(match.group(1)).path
            page = get_page_from_path(path)

            if page:
                disclaimer_page_id = page.pk

    if disclaimer_page_id == 558 or disclaimer_page_id == 571:
        # Convert links to /privacy/privacy-policy/ and
        # /privacy/website-privacy-policy/ to the
        # Generic Email Sign-Up Privacy Act Statement
        disclaimer_page_id = 1189

    data['disclaimer_page'] = disclaimer_page_id

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
        ('ask_cfpb', '0019_add_disclaimer_pagechooserblock_to_emailsignup'),
        (
            'regulations3k',
            '0019_add_disclaimer_pagechooserblock_to_emailsignup'
        ),
        ('v1', '0141_add_disclaimer_pagechooserblock_to_emailsignup')
    ]
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
