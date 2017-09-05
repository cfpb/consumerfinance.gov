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
rss_feed = {
    "type": "rss_feed",
    "value": "blog_feed"
}
featured_content = {
    'type': 'featured_content',
    'value': {
        'body': "this is a featured content body"
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
filter_controls = {
    'type': 'filter_controls',
    'value': {
            'is_expanded': False,
            'post_date_description': 'Published',
            'link_image_and_heading': False,
            'topics': True,
            'title': True,
            'label': '',
            'date_range': True,
            'is_midtone': False,
            'authors': True,
            'form_type': 'filterable-list',
            'is_bordered': False,
            'output_5050': False,
            'categories': {
                'show_preview_categories': True,
                'page_type': 'blog',
                'filter_category': True
            }
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
image_text_25_75_group = {
    "type": "image_text_25_75_group",
    "value": {
        "heading": "Image 25 75 Group",
        "image_texts": [
            {
                "heading": "",
                "body": "this is an image text in a 25 75 group",
                "has_rule": False,
                "image": {
                    "alt": "",
                    "upload": 84
                },
                "links": [
                    {
                        "url": "/",
                        "text": "test"
                    }
                ]
            }
        ]
    }
}
image_text_50_50_group = {
    "type": "image_text_50_50_group",
    "value": {
        "heading": "Image 50 50 Group",
        "image_texts": [
            {
                "heading": "",
                "body": "this is an image text in a 50 50 group",
                "links": [
                    {
                        "url": "/",
                        "text": "test"
                    }
                ],
                "image": {
                    "alt": "",
                    "upload": 84
                },
                "is_widescreen": False,
                "is_button": False
            }
        ]
    }
}
half_width_link_blob_group = {
    "type": "half_width_link_blob_group",
    "value": {
        "heading": "Half Width Link Blob Group",
        "link_blobs": [
            {
                "body": "this is a half width link blob",
                "heading": "",
                "links": [
                    {
                        "url": "/",
                        "text": "test"
                    }
                ]
            }
        ]
    }
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

html_block = {
    "type": "html_block",
    "value": {
        "html_url": "http://raw.githubusercontent.com/cfpb/consumer-credit-trends/master/charts/auto-loans/borrower-age/figure-4a__30-to-44__auto-loans.html"  # noqa
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
        "heading": "Test Snippet List",
        "snippet_type": "v1.models.snippets.Resource",
        "show_thumbnails": False,
    }
}

snippet_list_show_thumbnails_true = {
    "type": "snippet_list",
    "value": {
        "heading": "Test Snippet List",
        "snippet_type": "v1.models.snippets.Resource",
        "show_thumbnails": True,
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

job_listing_list = {
    'type': 'job_listing_list',
    'value': {
        'limit': 5,
        'more_jobs_page': 123,
        'hide_closed': True,
        'heading': 'heading',
        'more_jobs_text': 'Full list of jobs',
    },
}

job_listing_table = {
    'type': u'job_listing_table',
    'value': {
        'is_striped': False,
        'hide_closed': True,
        'is_full_width': False,
        'is_stacked': False,
        'first_row_is_table_header': True,
        'first_col_is_header': False,
    },
}

conference_registration_form = {
    'type': 'conference_registration_form',
    'value': {
        'at_capacity_message': [
            {
                'type': 'content',
                'value': 'Full.',
            },
        ],
        'code': 'GDCODE',
        'capacity': 100,
        'failure_message': 'Oops.',
        'heading': 'Register.',
        'sessions': ['Morning', 'Afternoon'],
        'success_message': 'Success!',
    },
}

data_snapshot = {
    'type': u'data_snapshot',
    'value': {
        'market_key': u'AUT',
        'num_originations': u'5 million',
        'value_originations': u'$64 billion',
        'year_over_year_change': u'5% increase',
        'last_updated_projected_data': u'2015-01-01',
        'num_originations_text': u'Auto loans originated',
        'value_originations_text': u'Dollar value of new loans',
        'year_over_year_change_text': u'In year-over-year originations',
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
        'note': 'Data not final',
    }
}
