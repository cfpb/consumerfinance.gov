from corsheaders.signals import check_request_enabled


def cors_allow_particular_urls(sender, request, **kwargs):
    """Allow all requests starting with given path to bypass CORS

    In other words, it makes the college costs API endpoints truly public APIs,
    instead of restricting access to requests from consumerfinance.gov.

    Based on this example in the django-cors-headers docs:
    https://github.com/adamchainz/django-cors-headers#signals
    """
    return request.path.startswith(
        "/paying-for-college2/understanding-your-financial-aid-offer/api/"
    )


check_request_enabled.connect(cors_allow_particular_urls)
