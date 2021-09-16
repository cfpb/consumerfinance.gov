call_to_action_defaults = {
    'slug_text': 'Take action',
    'paragraph_text': 'Click this button.',
    'button': {
        'text': 'Click me',
    },
}


call_to_action_test_cases = {
    'Default': {},

    'External link': {
        'button': {
            'text': 'External link',
            'url': 'https://example.com',
        },
    },

    'Download': {
        'button': {
            'text': 'Download me',
            'url': '/something.pdf',
        },
    },
}


for test_case in call_to_action_test_cases.values():
    for k, v in call_to_action_defaults.items():
        test_case.setdefault(k, v)
