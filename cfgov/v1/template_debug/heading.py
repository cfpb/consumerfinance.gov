heading_defaults = {
    'text': 'This is a heading.',
}


heading_test_cases = {
    'Text only': {},

    'No text (should render nothing)': {
        'text': None,
    },

    'Different heading level (H2)': {
        'level': 'h2',
    },

    'Different heading class (H3 rendered as H2)': {
        'level_class': 'h2',
    },

    'Icon': {
        'icon': 'pencil',
    },
}


for test_case in heading_test_cases.values():
    for k, v in heading_defaults.items():
        test_case.setdefault(k, v)
