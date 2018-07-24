from core.utils import parse_links, should_parse_links


class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


class ParseLinksMiddleware(object):
    def process_response(self, request, response):
        if should_parse_links(request.path, response['content-type']):
            response.content = parse_links(response.content)
        return response
