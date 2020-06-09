# -*- coding: utf-8 -*-
featured_content_defaults = {
    'heading': 'Featured content',
    'body': (
        'Lorem ipsum dolor sit amet, ei ius adhuc inani iudico, labitur '
        'instructior ex pri. Cu pri inani constituto, cum aeque noster '
        'commodo cu.'
    ),
    'links': [
        {
            'text': 'Consumer Financial Protection Bureau',
            'url': 'https://www.consumerfinance.gov',
        },
    ],
}


FEATURED_CONTENT_IMAGE_URL = (
    'https://files.consumerfinance.gov/f/images/'
    'cfpb_buying-a-home_carousel.original.png'
)


featured_content_test_cases = {
    'Image': {
        'image': {'url': FEATURED_CONTENT_IMAGE_URL},
    },

    'Image with alt text': {
        'image': {
            'url': FEATURED_CONTENT_IMAGE_URL,
            'alt_text': 'This is image alt text',
        },
    },

    'Multiple links': {
        'image': {'url': FEATURED_CONTENT_IMAGE_URL},
        'links': [
            {
                'text': 'Consumer Financial Protection Bureau',
                'url': 'https://www.consumerfinance.gov',
            },
            {
                'text': 'Oficina para la Protección Financiera del Consumidor',
                'url': 'https://www.consumerfinance.gov/es/',
            },
        ],
    },

    'Video': {
        'video': {'video_id': 'dQw4w9WgXcQ'},
    },

    'Video with custom thumbnail': {
        'video': {
            'video_id': 'dQw4w9WgXcQ',
            'thumbnail_url': FEATURED_CONTENT_IMAGE_URL,
        },
    },
}


for test_case in featured_content_test_cases.values():
    for k, v in featured_content_defaults.items():
        test_case.setdefault(k, v)
