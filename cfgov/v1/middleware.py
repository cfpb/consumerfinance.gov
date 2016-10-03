from django.conf import settings


class StagingMiddleware(object):
    def process_request(self, request):
        request_hostname = getattr(request.site, 'hostname', None)
        request.is_staging = request_hostname == settings.STAGING_HOSTNAME
