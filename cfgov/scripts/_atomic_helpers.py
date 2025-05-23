#############
# Molecules #
#############

contact_email = {
    "type": "email",
    "value": {"emails": [{"url": "test@example.com", "text": "e-mail"}]},
}
contact_phone = {
    "type": "phone",
    "value": {
        "phones": [
            {
                "tty": "",
                "number": "5151234567",
                "extension": "1234",
                "vanity": "",
            }
        ],
        "fax": True,
    },
}
contact_address = {
    "type": "address",
    "value": {
        "city": "Washington",
        "title": "",
        "label": "Address",
        "state": "DC",
        "street": "123 abc street",
        "zip_code": "20012",
    },
}
related_links = {
    "type": "related_links",
    "value": {"links": [{"url": "/url", "text": "this is a related link"}]},
}
expandable = {
    "type": "expandable",
    "value": {"label": "this is an expandable"},
}
text_introduction = {
    "type": "text_introduction",
    "value": {"intro": "this is an intro"},
}
hero = {"type": "hero", "value": {"heading": "this is a hero heading"}}
notification = {
    "type": "notification",
    "value": {
        "message": "this is a notification message",
        "explanation": "this is a notification explanation",
        "links": [{"url": "/", "text": "this is a notification link"}],
    },
}
related_metadata = {
    "type": "related_metadata",
    "value": {
        "content": [
            {
                "type": "text",
                "value": {"heading": "this is a related metadata heading"},
            }
        ]
    },
}
call_to_action = {
    "type": "call_to_action",
    "value": {"paragraph_text": "this is a call to action"},
}

#############
# Organisms #
#############

main_contact_info = lambda contact_id: {
    "type": "contact",
    "value": {"contact": contact_id},
}
sidebar_contact = lambda contact_id: {
    "type": "sidebar_contact",
    "value": {"contact": contact_id},
}
well = {"type": "well", "value": {"content": "this is well content"}}
full_width_text = {
    "type": "full_width_text",
    "value": [
        {
            "type": "content_with_anchor",
            "value": {
                "content_block": "full width text block",
                "anchor_link": {"link_id": "this is an anchor link"},
            },
        },
        {
            "type": "quote",
            "value": {"body": "this is a quote", "citation": "a citation"},
        },
        {"type": "content", "value": "Full width text content"},
    ],
}

info_unit_group = {
    "type": "info_unit_group",
    "value": {
        "heading": {
            "text": "Info Unit Group",
        },
        "info_units": [
            {
                "body": "this is an info unit",
                "links": [{"url": "/", "text": "test"}],
            }
        ],
    },
}

table_block = {
    "type": "table_block",
    "value": {
        "data": [
            ["Header One", "Header Two", "Header Three", "Header Four"],
            ["Row 1-1", "Row 1-2", "Row 1-3", "Row 1-4"],
            ["Row 2-1", "Row 2-2", "Row 2-3", "Row 2-4"],
        ],
        "first_row_is_table_header": True,
        "first_col_is_header": False,
    },
}

expandable_group = {
    "type": "expandable_group",
    "value": {
        "heading": "Expandable Group",
        "body": "<p>Expandable group body.</p>",
        "is_accordion": False,
        "has_rule": False,
        "expandables": [expandable] * 3,
    },
}
item_introduction = {
    "type": "item_introduction",
    "value": {
        "category": "testimony",
        "heading": "Item Introduction",
        "paragraph": "<p>Item introduction body.</p>",
        "date": "2016-05-18T16:49:00Z",
        "has_social": False,
    },
}

data_snapshot = {
    "type": "data_snapshot",
    "value": {
        "market_key": "STU",
        "num_originations": "5 million",
        "value_originations": "$64 billion",
        "year_over_year_change": "5% increase",
        "last_updated_projected_data": "2015-01-01",
        "num_originations_text": "Loans originated",
        "value_originations_text": "Dollar value of new loans",
        "year_over_year_change_text": "In year-over-year originations",
        "inquiry_month": "",
        "inquiry_year_over_year_change": "",
        "inquiry_year_over_year_change_text": "",
        "tightness_month": "",
        "tightness_year_over_year_change": "",
        "tightness_year_over_year_change_text": "",
    },
}

data_snapshot_with_optional_fields = {
    "type": "data_snapshot",
    "value": {
        "market_key": "AUT",
        "num_originations": "5 million",
        "value_originations": "$64 billion",
        "year_over_year_change": "5% increase",
        "last_updated_projected_data": "2015-01-01",
        "num_originations_text": "Loans originated",
        "value_originations_text": "Dollar value of new loans",
        "year_over_year_change_text": "In year-over-year originations",
        "inquiry_month": "2015-01-01",
        "inquiry_year_over_year_change": "7.4% decrease",
        "inquiry_year_over_year_change_text": "In year-over-year inquiries",
        "tightness_month": "2015-01-01",
        "tightness_year_over_year_change": "2.8% increase",
        "tightness_year_over_year_change_text": "In year-over-year credit tightness",  # noqa
    },
}

chart_block = {
    "type": "chart_block",
    "value": {
        "title": "Volume of credit cards originated",
        "chart_type": "Line",
        "color_scheme": "Green",
        "data_source": "foo/bar.csv",
        "date_published": "2018-01-01",
        "description": "Description",
        "last_updated_projected_data": "2016-04-01",
        "note": "Data not final.",
    },
}

chart_block_inquiry_activity = {
    "type": "chart_block",
    "value": {
        "title": "Indexed number of consumers with inquiries (beta)",
        "chart_type": "line-index",
        "color_scheme": "Purple",
        "data_source": "consumer-credit-trends/credit-cards/inq_data_CRC.csv",
        # should get overwritten by data_snapshot.json
        "date_published": "2001-01-01",
        "description": "Indexed number of people with credit card inquiries.",
        "note": "Data from the last four months are not final.",
    },
}

chart_block_credit_tightness = {
    "type": "chart_block",
    "value": {
        "title": "Indexed number of consumers with credit tightness (beta)",
        "chart_type": "line-index",
        "color_scheme": "Purple",
        "data_source": "consumer-credit-trends/credit-cards/crt_data_CRC.csv",
        # should get overwritten by data_snapshot.json
        "date_published": "2001-01-01",
        "description": "Indexed number of people who applied for credit cards but did not open a new account.",  # noqa
        "note": "Data from the last four months are not final.",
    },
}
