from django.utils.safestring import mark_safe


notification_defaults = {
    "type": "warning",
    "is_visible": True,
    "message": "This is a test notification.",
    "explanation": None,
    "links": [],
}


message_with_html_tags = (
    'Visit <a href="https://www.consumerfinance.gov/">' "www.consumerfinance.gov</a>."
)


consumer_tools_message = "Consumer tools"


consumer_tools_explanation = (
    "Wherever you are on your financial journey, you can prepare yourself "
    "to make informed financial decisions with these resources."
)


consumer_tools_links = [
    {
        "text": "Auto loans",
        "url": "https://www.consumerfinance.gov/consumer-tools/auto-loans/",
    },
    {
        "text": "Bank accounts & services",
        "url": "https://www.consumerfinance.gov/consumer-tools/bank-accounts/",
    },
    {
        "text": "Credit cards",
        "url": "https://www.consumerfinance.gov/consumer-tools/credit-cards/",
    },
]


notification_test_cases = {
    "Warning message": {},
    "Success message": {
        "type": "success",
    },
    "Error message": {
        "type": "error",
    },
    "Message including Unicode characters": {
        "message": 'Use “curly quotes” instead of "straight quotes".',
    },
    "Message including raw HTML tags": {
        "message": message_with_html_tags,
    },
    "Message including HTML tags passed through mark_safe": {
        "message": mark_safe(message_with_html_tags),
    },
    "Long message": {
        "message": (
            "Some people, when confronted with a problem, think “I know, "
            "I'll use regular expressions.” Now they have two problems."
        ),
    },
    "Message with explanation": {
        "message": consumer_tools_message,
        "explanation": consumer_tools_explanation,
    },
    "Message with links": {
        "message": consumer_tools_message,
        "links": consumer_tools_links,
    },
    "Message with explanation and links": {
        "message": consumer_tools_message,
        "explanation": consumer_tools_explanation,
        "links": consumer_tools_links,
    },
    "Invisible": {
        "is_visible": False,
    },
}


for test_case in notification_test_cases.values():
    for k, v in notification_defaults.items():
        test_case.setdefault(k, v)
