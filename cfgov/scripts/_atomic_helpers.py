contact_email = {
    "type": "email",
    "value": {
        "emails": [
            {
                "url": "/",
                "text": "test@example.com"
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
                "number": "1234567890",
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
image_text_25_75_group = {
    "type": "image_text_25_75_group",
     "value": {
        "heading": "Image 25 75 Group", "image_texts": [
            {
                "heading": "",
                "body": "",
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
},
image_text_50_50_group = {
    "type": "image_text_50_50_group",
    "value": {
        "heading": "Image 50 50 Group",
        "image_texts": [
            {
                "heading": "",
                "body": "",
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
},
half_width_link_blob_group = {
    "type": "half_width_link_blob_group",
    "value": {
        "heading": "Half Width Link Blob Group",
        "link_blobs": [
            {
                "body": "",
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
contact = lambda contact_id: {
    "type": "contact",
    "value": {
        "body": "",
        "header": "Contact",
        "contact": contact_id
    }
}
email_signup = {
    "type": "email_signup",
    "value": {
        "text": "",
        "gd_code": "",
        "heading": "Email Sign Up",
        "form_field": [
            {
                "info": "",
                "type": "",
                "required": False,
                "label": "Email Sign up",
                "btn_text": "",
                "placeholder": ""
            }
        ]
    }
},
rss_feed = {
    "type": "rss_feed",
    "value": "blog_feed"
}
featured_content = {
    'type': 'featured_content',
    'value': {
        'body': "<p>this is a featured content body</p>"
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
full_width_text = {
    'type': 'full_width_text',
    'value': [
        {
            'type': 'quote',
            'value': {
                'body': 'this is a quote',
                'citation': 'a citation'
            }
        }
    ]
},
call_to_action = {
    'type': 'call_to_action',
    'value': {
        'paragraph_text': 'this is a call to action'
    }
}
