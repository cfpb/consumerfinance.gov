class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


class CSPScriptHashMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request, 'script_hashes'):
            for header in ('content-security-policy',
                           'content-security-policy-report-only'):
                if header in response._headers:
                    csp_name, csp = response._headers[header]
                    hashes = ' '.join(request.script_hashes)
                    csp = csp.replace('script-src', 'script-src ' + hashes)

                    response._headers[header] = (csp_name, csp)

        return response
