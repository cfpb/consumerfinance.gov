from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from wagtail.contrib.wagtailfrontendcache.utils import purge_url_from_cache

from requests.exceptions import HTTPError
from v1.admin_forms import AkamaiFlushForm
from v1.models.akamai_backend import AkamaiBackend


def cdn_is_configured():
    return (hasattr(settings, 'WAGTAILFRONTENDCACHE') and
            settings.WAGTAILFRONTENDCACHE)


def purge(request, url=None):
    if url:
        purge_url_from_cache(url)
        messages.success(request,
                         "flushing %s" % url)
    else:
        config = settings.WAGTAILFRONTENDCACHE['akamai']
        backend = AkamaiBackend(config)
        backend.purge_all()
        messages.success(request,
                         "flushed entire site")


def manage_cdn(request):
    if not cdn_is_configured():
        return render(request, 'cdnadmin/disabled.html')

    if request.method == 'GET':
        form = AkamaiFlushForm()
    elif request.method == 'POST':
        form = AkamaiFlushForm(request.POST)
        if form.is_valid():
            try:
                purge(request, form.cleaned_data['url'])
            except Exception as e:
                if isinstance(e, HTTPError):
                    error_info = e.response.json()
                    error_message = "{title}: {detail}".format(**error_info)
                else:
                    error_message = repr(e)
                messages.error(request, error_message)
        else:
            for field, error_list in form.errors.iteritems():
                for error in error_list:
                    messages.error(request, "Error in %s: %s" % (field, error))
    return render(request, 'cdnadmin/index.html', context={'form': form})
