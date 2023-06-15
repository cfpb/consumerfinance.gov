table_defaults = {
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
    "No headings": {
        "data": {
            "rows": table_defaults["data"]["rows"],
        }
    },
    "Stack on mobile": {
        "options": ["stack_on_mobile"],
    },
}


for test_case in table_test_cases.values():
    for k, v in table_defaults.items():
        test_case.setdefault(k, v)
