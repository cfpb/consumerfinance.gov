from django.utils.safestring import mark_safe


table_defaults = {
    "heading": "",
    "data": {
        "columns": [
            {"heading": "Column 1"},
            {"heading": "Column 2"},
        ],
        "rows": [
            ["0,0", "0,1"],
            ["1,0", "1,1"],
        ],
    },
}


table_test_cases = {
    "Default": {},
    "No header row": {
        "data": {
            "columns": [
                {"heading": ""},
                {"heading": ""},
            ],
            "rows": table_defaults["data"]["rows"],
        }
    },
    "Full width": {
        "options": ["is_full_width"],
    },
    "Stack on mobile": {
        "options": ["stack_on_mobile"],
    },
    "Stack on mobile, no column headings": {
        "options": ["stack_on_mobile"],
        "data": {
            "columns": [
                {"heading": ""},
                {"heading": ""},
            ],
            "rows": [
                ["0,0", "0,1"],
                ["1,0", "1,1"],
            ],
        },
    },
    "With heading": {
        "heading": mark_safe("<h3>This is a table</h3>"),
    },
    "First column header": {"options": ["first_column_header"]},
    "First column header, no column headings": {
        "data": {
            "columns": [
                {"heading": ""},
                {"heading": ""},
                {"heading": ""},
            ],
            "rows": [
                ["A", "0,0", "0,1"],
                ["B", "1,0", "1,1"],
            ],
        },
        "options": ["first_column_header"],
    },
}


for test_case in table_test_cases.values():
    for k, v in table_defaults.items():
        test_case.setdefault(k, v)


crc_table_test_cases = {
    "Default": {
        "website": mark_safe(
            '<a href="https://example.com/">https://example.com/</a>'
        ),
        "phone": mark_safe('<a href="tel:202-555-1234">(202) 555-1234</a>'),
        "mailing_address": mark_safe(
            "Example, Inc.<br/>" "P.O. Box 8000<br/>" "Washington, DC 20001"
        ),
    }
}


contact_us_table_test_cases = {
    "Default": {
        "heading": "This is a Contact Us table",
        "rows": [
            {
                "title": "Item 1",
                "body": mark_safe(
                    '<a href="https://example.com/">https://example.com/</a>'
                ),
            },
            {
                "title": "Item 2",
                "body": mark_safe("Foo<br/>Bar"),
            },
        ],
    },
}
