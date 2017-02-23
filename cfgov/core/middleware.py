class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response
