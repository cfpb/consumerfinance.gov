import logging

from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from wagtail.contrib.wagtailfrontendcache.utils import PurgeBatch

from requests.exceptions import HTTPError

from v1.admin_forms import CacheInvalidationForm
from v1.models.caching import AkamaiBackend, CDNHistory


logger = logging.getLogger(__name__)


def cdn_is_configured():
    return (hasattr(settings, 'WAGTAILFRONTENDCACHE') and
            settings.WAGTAILFRONTENDCACHE)


def purge(url=None):
    akamai_config = settings.WAGTAILFRONTENDCACHE.get('akamai', {})
    cloudfront_config = settings.WAGTAILFRONTENDCACHE.get('files', {})

    if url:
        # Use the Wagtail frontendcache PurgeBatch to perform the purge
        batch = PurgeBatch()
        batch.add_url(url)

        # If the URL matches any of our CloudFront distributions, invalidate
        # with that backend
        if any(k for k in cloudfront_config.get('DISTRIBUTION_ID', {})
               if k in url):
            logger.info('Purging {} from "files" cache'.format(url))
            batch.purge(backends=['files'])

        # Otherwise invalidate with our default backend
        else:
            logger.info('Purging {} from "akamai" cache'.format(url))
            batch.purge(backends=['akamai'])

        return "Submitted invalidation for %s" % url

    else:
        # purge_all only exists on our AkamaiBackend
        backend = AkamaiBackend(akamai_config)
        logger.info('Purging entire site from "akamai" cache')
        backend.purge_all()
        return "Submitted invalidation for the entire site."


def manage_cdn(request):
    if not cdn_is_configured():
        return render(request, 'cdnadmin/disabled.html')

    user_can_purge = request.user.has_perm('v1.add_cdnhistory')

    if request.method == 'GET':
        form = CacheInvalidationForm()

    elif request.method == 'POST':
        if not user_can_purge:
            return HttpResponseForbidden()

        form = CacheInvalidationForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            history_item = CDNHistory(subject=url or "entire site",
                                      user=request.user)

            try:
                message = purge(url)
                history_item.message = message
                history_item.save()
                messages.success(request, message)
            except Exception as e:
                if isinstance(e, HTTPError):
                    error_info = e.response.json()
                    error_message = "{title}: {detail}".format(**error_info)
                else:
                    error_message = repr(e)

                history_item.message = error_message
                history_item.save()
                messages.error(request, error_message)

        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, "Error in %s: %s" % (field, error))

    history = CDNHistory.objects.all().order_by('-created')[:20]
    return render(request, 'cdnadmin/index.html',
                  context={'form': form,
                           'user_can_purge': user_can_purge,
                           'history': history})
