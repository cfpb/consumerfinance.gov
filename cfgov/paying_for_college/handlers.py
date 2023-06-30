from corsheaders.signals import check_request_enabled

def cors_allow_particular_urls(sender, request, **kwargs):
    return request.path.startswith('/paying-for-college2/understanding-your-financial-aid-offer/api/')

check_request_enabled.connect(cors_allow_particular_urls)
