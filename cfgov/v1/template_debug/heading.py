heading_defaults = {
    'text': 'This is a heading.',
    'level': 'h3',
}


heading_test_cases = {
    'H3': {},

    'H3, no text (should render nothing)': {
        'text': None,
    },

    'H2': {
        'level': 'h2',
    },

    'H3 rendered as H2': {
        'level_class': 'h2',
    },

    'H3 with icon': {
        'icon': 'pencil',
    },
}


for test_case in heading_test_cases.values():
    for k, v in heading_defaults.items():
        test_case.setdefault(k, v)
