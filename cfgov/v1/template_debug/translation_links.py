links = [
    {
        "href": "/en/",
        "language": "en",
        "text": "English",
    },
    {
        "href": "/es/",
        "language": "es",
        "text": "Español",
    },
    {
        "href": "/zh-Hant/",
        "language": "zh-Hant",
        "text": "中文",
    },
    {
        "href": "/vi/",
        "language": "vi",
        "text": "Tiếng Việt",
    },
    {
        "href": "/ko/",
        "language": "ko",
        "text": "한국어",
    },
    {
        "href": "/tl/",
        "language": "tl",
        "text": "Tagalog",
    },
    {
        "href": "/ru/",
        "language": "ru",
        "text": "Pусский",
    },
    {
        "href": "/ar/",
        "language": "ar",
        "text": "العربية",
    },
    {
        "href": "/ht/",
        "language": "ht",
        "text": "Kreyòl Ayisyen",
    },
]

translation_links_test_cases = {
    "No translations": {
        "page": {"links": []},
    },
    "English page with Spanish translation": {
        "language": "en",
        "links": links[:2],
    },
    "Spanish page with English translation": {
        "language": "es",
        "links": links[:2],
    },
}

for link in links:
    translation_links_test_cases[
        f"{link['text']} page with all translations"
    ] = {
        "language": link["language"],
        "links": links,
    }
