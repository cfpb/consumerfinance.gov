from django.conf import settings

from core.utils import parse_links


class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


class ParseLinksMiddleware(object):
    def process_response(self, request, response):
        # Do not parse links for paths in the blacklist
        for path in settings.PARSE_LINKS_BLACKLIST:
            if request.path.startswith(path):
                return response

        response.content = parse_links(response.content)
        return response
