from core.utils import parse_links


class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


class AddExternalLinkRedirectsMiddleware(object):
    def process_response(self, request, response):
        response.content = parse_links(response.content)
        return response
