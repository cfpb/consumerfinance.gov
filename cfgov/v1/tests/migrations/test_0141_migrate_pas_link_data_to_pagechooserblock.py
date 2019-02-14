from importlib import import_module

from unittest import TestCase


class TestMigration0141(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMigration0141, cls).setUpClass()
        cls.migration = import_module(
            'v1.migrations.0141_migrate_pas_link_data_to_pagechooserblock'
        )

    def test_forward_mapper(self):
        data = {'text': u'Our email newsletter has tips and info to help you through the process.', 'gd_code': u'USCFPB_127', 'heading': u'Buying a home?', 'form_field': [{'info': u'<p><a id="3775" linktype="page">Privacy Act statement</a><br/></p>', 'inline_info': True, 'required': True, 'label': u'Email address', 'btn_text': u'Sign up', 'placeholder': u'example@mail.com', 'type': u'email'}], 'default_heading': False}

        migrated = self.migration.forward_mapper(
            'unused param',
            data
        )
        # import pdb; pdb.set_trace()

        self.assertEqual(migrated, {
            'heading': u'Buying a home?',
            'default_heading': False,
            'text': u'Our email newsletter has tips and info to help you through the process.',
            'gd_code': u'USCFPB_127',
            'disclaimer_page': 3775,
            'form_field': [{
                'type': u'email',
                'inline_info': True,
                'btn_text': u'Sign up',
                'info': u'<p><a id="3775" linktype="page">Privacy Act statement</a><br/></p>',
                'label': u'Email address',
                'required': True,
                'placeholder': u'example@mail.com'
            }]
        })
