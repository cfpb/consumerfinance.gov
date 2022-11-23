from django.utils import timezone


today = timezone.now().date()


item_introduction_defaults = {
    "heading": "Lorem ipsum dolor sit amet",
    "paragraph": (
        "<p>Ut enim ad minim veniam, quis nostrud exercitation ullamco "
        "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
        "dolor in reprehenderit in voluptate velit esse cillum dolore eu "
        "fugiat nulla pariatur.</p>"
    ),
    "has_social": True,
}


category = {
    "show_category": True,
    "category": "press-release",
    "category_url": "/about-us/newsroom/",
}


byline = {
    "authors": ["Bilbo Baggins"],
    "date": today,
}


item_introduction_test_cases = {
    "Heading and paragraph": {},
    "Category": category,
    "Byline": byline,
    "Everything": {**category, **byline},
    "Customized social icons": {
        "social_options": {
            "is_printable": True,
        },
    },
}


for test_case in item_introduction_test_cases.values():
    for k, v in item_introduction_defaults.items():
        test_case.setdefault(k, v)
