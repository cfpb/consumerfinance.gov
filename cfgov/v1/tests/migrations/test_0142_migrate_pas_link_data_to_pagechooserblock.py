from importlib import import_module

from unittest import TestCase

from v1.models.base import CFGOVPage
from v1.tests.wagtail_pages.helpers import save_new_page


class TestMigration0142(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMigration0142, cls).setUpClass()
        cls.migration = import_module(
            'v1.migrations.0142_migrate_pas_link_data_to_pagechooserblock'
        )

    def test_forward_mapper_internal_pas_link(self):
        # data comes from EmailSignup block inside FullWidthText on page 11358
        data = {
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'heading': u'Buying a home?',
            'form_field': [{
                'info': u'<p><a id="3775" linktype="page">PAS</a></p>',
                'inline_info': True,
                'required': True,
                'label': u'Email address',
                'btn_text': u'Sign up',
                'placeholder': u'example@mail.com',
                'type': u'email'
            }],
            'default_heading': False
        }

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': 3775,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<p><a id="3775" linktype="page">PAS</a></p>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })

    def test_forward_mapper_explicit_path_pas_link(self):
        page = CFGOVPage(
            title='Privacy Act statement',
            slug='privacy-act-statement',
        )
        save_new_page(page)

        data = {
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'heading': u'Buying a home?',
            'form_field': [{
                'info': u'<p><a href="/privacy-act-statement/">PAS</a></p>',
                'inline_info': True,
                'required': True,
                'label': u'Email address',
                'btn_text': u'Sign up',
                'placeholder': u'example@mail.com',
                'type': u'email'
            }],
            'default_heading': False
        }

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': page.pk,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<p><a href="/privacy-act-statement/">PAS</a></p>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })

    def test_forward_mapper_no_pas_link_gets_generic(self):
        data = {
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'heading': u'Buying a home?',
            'form_field': [{
                'info': u'<p>Who needs a disclaimer?</p>',
                'inline_info': True,
                'required': True,
                'label': u'Email address',
                'btn_text': u'Sign up',
                'placeholder': u'example@mail.com',
                'type': u'email'
            }],
            'default_heading': False
        }

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': 1189,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<p>Who needs a disclaimer?</p>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })

    def test_forward_mapper_wrong_generic_links_get_correct_generic_link(self):
        self.maxDiff = None

        data = {
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'heading': u'Buying a home?',
            'form_field': [{
                'info': u'<a id="558" linktype="page">Privacy Policy</a>',
                'inline_info': True,
                'required': True,
                'label': u'Email address',
                'btn_text': u'Sign up',
                'placeholder': u'example@mail.com',
                'type': u'email'
            }],
            'default_heading': False
        }

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': 1189,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<a id="558" linktype="page">Privacy Policy</a>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })

        data = {
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'heading': u'Buying a home?',
            'form_field': [{
                'info': u'<a id="571" linktype="page">'
                        'Website Privacy Policy</a>',
                'inline_info': True,
                'required': True,
                'label': u'Email address',
                'btn_text': u'Sign up',
                'placeholder': u'example@mail.com',
                'type': u'email'
            }],
            'default_heading': False
        }

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you ...',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': 1189,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<a id="571" linktype="page">'
                        'Website Privacy Policy</a>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })
