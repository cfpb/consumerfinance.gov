from django.utils import timezone


today = timezone.now().date()


byline_test_cases = {
    "Empty": {},
    "Single author": {
        "authors": [
            "Bilbo Baggins",
        ],
    },
    "Two authors": {
        "authors": [
            "Bilbo Baggins",
            "Frodo Baggins",
        ],
    },
    "Three authors": {
        "authors": [
            "Bilbo Baggins",
            "Frodo Baggins",
            "Samwise Gamgee",
        ],
    },
    "Author with date": {
        "authors": [
            "Bilbo Baggins",
        ],
        "date": today,
    },
    "Date, no authors": {
        "date": today,
    },
}
