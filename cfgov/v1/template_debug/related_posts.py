from datetime import timedelta

from django.utils import timezone


def _make_posts(name):
    now = timezone.now()

    return [
        {
            "title": f"{name.title()} {i}",
            "url": f"/{name}s/{i}/",
            "date": now - timedelta(days=3 - i),
        }
        for i in range(3, 0, -1)
    ]


reports = {
    "title": "Reports",
    "icon": "chart",
    "posts": _make_posts("report"),
}


events = {
    "title": "Events",
    "icon": "date",
    "posts": _make_posts("event"),
}


related_posts_defaults = {
    "header_title": "Read more",
    "show_heading": True,
    "posts": [reports, events],
    "view_more_url": "/related/",
}


related_posts_test_cases = {
    "Multiple lists": {},
    "Single list": {
        "posts": [reports],
    },
    "Limit 1": {
        "limit": 1,
    },
    "Hide heading": {
        "show_heading": False,
    },
}


for test_case in related_posts_test_cases.values():
    for k, v in related_posts_defaults.items():
        test_case.setdefault(k, v)
