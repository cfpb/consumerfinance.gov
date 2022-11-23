from django.utils import timezone


today = timezone.now().date()


text_introduction_defaults = {
    "intro": (
        "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
        "eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>"
    ),
    "body": (
        "<p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris"
        " nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
        "culpa qui officia deserunt mollit anim id est laborum.</p>"
    ),
}


heading = {
    "heading": "Local hobbit finishes lengthy journey",
}


eyebrow = {
    "eyebrow": "Press Release",
}


byline = {
    "authors": ["Bilbo Baggins"],
    "date": today,
}


links = {
    "links": [
        {
            "text": "Click me",
            "url": "https://www.consumerfinance.gov/",
            "aria-label": "CFPB website",
        }
    ],
}


text_introduction_test_cases = {
    "With heading": heading,
    "With heading and eyebrow": {**heading, **eyebrow},
    "With byline": byline,
    "With link": links,
    "With everything": {**heading, **eyebrow, **byline, **links},
}


for test_case in text_introduction_test_cases.values():
    for k, v in text_introduction_defaults.items():
        test_case.setdefault(k, v)
