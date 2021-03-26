#############
# Molecules #
#############

contact_email = {
    "type": "email",
    "value": {
        "emails": [
            {
                "url": "test@example.com",
                "text": "e-mail"
            }
        ]
    }
}
contact_phone = {
    "type": "phone",
    "value": {
        "phones": [
            {
                "tty": "",
                "number": "5151234567",
                "extension": "1234",
                "vanity": ""
            }
        ],
        "fax": True
    }
}
contact_address = {
    "type": "address",
    "value": {
        "city": "Washington",
        "title": "",
        "label": "Address",
        "state": "DC",
        "street": "123 abc street",
        "zip_code": "20012"
    }
}
related_links = {
    'type': 'related_links',
    'value': {
        'links': [
            {
                'url': '/url',
                'text': 'this is a related link'
            }
        ]
    }
}
expandable = {
    'type': 'expandable',
    'value': {
        'label': 'this is an expandable'
    }
}
text_introduction = {
    'type': 'text_introduction',
    'value': {
        'intro': 'this is an intro'
    }
}
hero = {
    'type': 'hero',
    'value': {
        'heading': "this is a hero heading"
    }
}
notification = {
    'type': 'notification',
    'value': {
        'message': "this is a notification message",
        'explanation': "this is a notification explanation",
        'links': [
            {
                "url": "/",
                "text": "this is a notification link"
            }
        ]
    }
}
related_metadata = {
    'type': 'related_metadata',
    'value': {
        'content': [
            {
                'type': 'text',
                'value': {
                    'heading': 'this is a related metadata heading'
                }
            }
        ]
    }
}
call_to_action = {
    'type': 'call_to_action',
    'value': {
        'paragraph_text': 'this is a call to action'
    }
}

#############
# Organisms #
#############

main_contact_info = lambda contact_id: {
    'type': 'contact',
    'value': {
        'contact': contact_id
    }
}
sidebar_contact = lambda contact_id: {
    'type': 'sidebar_contact',
    'value': {
        'contact': contact_id
    }
}
well = {
    'type': 'well',
    'value': {
        'content': "this is well content"
    }
}
full_width_text = {
    'type': 'full_width_text',
    'value': [
        {
            'type': 'content_with_anchor',
            'value': {
                'content_block': 'full width text block',
                'anchor_link': {
                    'link_id': 'this is an anchor link'
                }
            }
        },
        {
            'type': 'quote',
            'value': {
                'body': 'this is a quote',
                'citation': 'a citation'
            }
        },
        {
            'type': 'content',
            'value': 'Full width text content'
        }
    ]
}

info_unit_group = {
    "type": "info_unit_group",
    "value": {
        "heading": {
            "text": "Info Unit Group",
        },
        "info_units": [
            {
                "body": "this is an info unit",
                "links": [
                    {
                        "url": "/",
                        "text": "test"
                    }
                ],
            }
        ]
    }
}

email_signup = {
    'type': 'email_signup',
    'value': {
        'heading': 'Email Sign Up',
        'text': 'Sign up for our newsletter.',
        'gd_code': 'TEST-GD-CODE',
        'form_field': [
            {
                'btn_text': 'this is a form field with button',
                'required': False,
                'info': 'We will never share your email address.',
                'label': 'Learn more',
                'type': 'email',
                'placeholder': 'email@domain.com',
            }
        ]
    }
}

email_signup_required = {
    'type': 'email_signup',
    'value': {
        'heading': 'Email Sign Up',
        'text': 'Sign up for our newsletter.',
        'gd_code': 'TEST-GD-CODE',
        'form_field': [
            {
                'btn_text': 'this is a form field with button',
                'required': True,
                'info': 'We will never share your email address.',
                'label': 'Learn more',
                'type': 'email',
                'placeholder': 'email@domain.com',
            }
        ]
    }
}

reg_comment = {
    "type": "reg_comment",
    "value": {
        'document_id': 'test document id',
        'generic_regs_link': True,
        'id': 'test id',
    }
}

snippet_list_show_thumbnails_false = {
    "type": "snippet_list",
    "value": {
        "heading": "Test Resource List",
        "snippet_type": "v1.models.resources.Resource",
        "show_thumbnails": False,
    }
}

snippet_list_show_thumbnails_true = {
    "type": "snippet_list",
    "value": {
        "heading": "Test Resource List",
        "snippet_type": "v1.models.resources.Resource",
        "show_thumbnails": True,
    }
}

snippet_list_actions_column_width_40 = {
    "type": "snippet_list",
    "value": {
        "heading": "Test Resource List",
        "snippet_type": "v1.models.resources.Resource",
        "actions_column_width": "40",
    }
}

table_block = {
    'type': 'table_block',
    'value': {
        'data':
        [
            [
                'Header One',
                'Header Two',
                'Header Three',
                'Header Four'
            ],
            [
                'Row 1-1',
                'Row 1-2',
                'Row 1-3',
                'Row 1-4'
            ],
            [
                'Row 2-1',
                'Row 2-2',
                'Row 2-3',
                'Row 2-4'
            ],
        ],
        'first_row_is_table_header': True,
        'first_col_is_header': False,
    }
}

expandable_group = {
    'type': 'expandable_group',
    'value': {
        'heading': 'Expandable Group',
        'body': '<p>Expandable group body.</p>',
        'is_accordion': False,
        'has_rule': False,
        'expandables': [expandable] * 3
    }
}
item_introduction = {
    'type': 'item_introduction',
    'value': {
        'category': 'testimony',
        'heading': 'Item Introduction',
        'paragraph': '<p>Item introduction body.</p>',
        'date': '2016-05-18T16:49:00Z',
        'has_social': False
    }
}

data_snapshot = {
    'type': u'data_snapshot',
    'value': {
        'market_key': u'STU',
        'num_originations': u'5 million',
        'value_originations': u'$64 billion',
        'year_over_year_change': u'5% increase',
        'last_updated_projected_data': u'2015-01-01',
        'num_originations_text': u'Loans originated',
        'value_originations_text': u'Dollar value of new loans',
        'year_over_year_change_text': u'In year-over-year originations',
        'inquiry_month': u'',
        'inquiry_year_over_year_change': u'',
        'inquiry_year_over_year_change_text': u'',
        'tightness_month': u'',
        'tightness_year_over_year_change': u'',
        'tightness_year_over_year_change_text': u'',
    }
}

data_snapshot_with_optional_fields = {
    'type': u'data_snapshot',
    'value': {
        'market_key': u'AUT',
        'num_originations': u'5 million',
        'value_originations': u'$64 billion',
        'year_over_year_change': u'5% increase',
        'last_updated_projected_data': u'2015-01-01',
        'num_originations_text': u'Loans originated',
        'value_originations_text': u'Dollar value of new loans',
        'year_over_year_change_text': u'In year-over-year originations',
        'inquiry_month': u'2015-01-01',
        'inquiry_year_over_year_change': u'7.4% decrease',
        'inquiry_year_over_year_change_text': u'In year-over-year inquiries',
        'tightness_month': u'2015-01-01',
        'tightness_year_over_year_change': u'2.8% increase',
        'tightness_year_over_year_change_text': u'In year-over-year credit tightness',  # noqa
    }
}

chart_block = {
    'type': u'chart_block',
    'value': {
        'title': u'Volume of credit cards originated',
        'chart_type': u'Line',
        'color_scheme': u'Green',
        'data_source': u'foo/bar.csv',
        'date_published': u'2018-01-01',
        'description': u'Description',
        'last_updated_projected_data': u'2016-04-01',
        'note': 'Data not final.',
    }
}

chart_block_inquiry_activity = {
    'type': u'chart_block',
    'value': {
        'title': u'Indexed number of consumers with inquiries (beta)',
        'chart_type': u'line-index',
        'color_scheme': u'Purple',
        'data_source': u'consumer-credit-trends/credit-cards/inq_data_CRC.csv',
        # should get overwritten by data_snapshot.json
        'date_published': u'2001-01-01',
        'description': u'Indexed number of people with credit card inquiries.',
        'note': 'Data from the last four months are not final.',
    }
}

chart_block_credit_tightness = {
    'type': u'chart_block',
    'value': {
        'title': u'Indexed number of consumers with credit tightness (beta)',
        'chart_type': u'line-index',
        'color_scheme': u'Purple',
        'data_source': u'consumer-credit-trends/credit-cards/crt_data_CRC.csv',
        # should get overwritten by data_snapshot.json
        'date_published': u'2001-01-01',
        'description': u'Indexed number of people who applied for credit cards but did not open a new account.',  # noqa
        'note': 'Data from the last four months are not final.',
    }
}


filter_controls = {
    'type': u'filter_controls',
    'value': {
        'topic_filtering': u'sort_by_frequency',
        'categories': {
            'page_type': '',
        },
        'filter_children': True,
        'filter_siblings': False,
    }
}
