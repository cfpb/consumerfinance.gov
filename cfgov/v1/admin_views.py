from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from wagtail.contrib.wagtailfrontendcache.utils import purge_url_from_cache

from requests.exceptions import HTTPError

from v1.admin_forms import AkamaiFlushForm
from v1.models.akamai_backend import AkamaiBackend, AkamaiHistory


def cdn_is_configured():
    return (hasattr(settings, 'WAGTAILFRONTENDCACHE') and
            settings.WAGTAILFRONTENDCACHE)


def purge(url=None):
    if url:
        purge_url_from_cache(url)
        return "flushed %s" % url
    else:
        config = settings.WAGTAILFRONTENDCACHE['akamai']
        backend = AkamaiBackend(config)
        backend.purge_all()
        return "flushed entire site"


def manage_cdn(request):
    if not cdn_is_configured():
        return render(request, 'cdnadmin/disabled.html')

    user_can_purge = request.user.has_perm('v1.add_akamaihistory')

    if request.method == 'GET':
        form = AkamaiFlushForm()
    elif request.method == 'POST':
        if not user_can_purge:
            return HttpResponseForbidden()

        form = AkamaiFlushForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            history_item = AkamaiHistory(subject=url or "entire site",
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
    history = AkamaiHistory.objects.all().order_by('-created')[:20]
    return render(request, 'cdnadmin/index.html',
                  context={'form': form,
                           'user_can_purge': user_can_purge,
                           'history': history})
