video_player_defaults = {
    'video_id': 'dQw4w9WgXcQ',
}


video_player_test_cases = {
    'Default': {},

    'Play button at bottom right': {
        'button_pos': 'bottomRight',
    },

    'Custom thumbnail image': {
        'thumbnail_url': (
            'https://files.consumerfinance.gov/f/images/'
            'cfpb_buying-a-home_carousel.original.png'
        ),
    },
}


for test_case in video_player_test_cases.values():
    for k, v in video_player_defaults.items():
        test_case.setdefault(k, v)
