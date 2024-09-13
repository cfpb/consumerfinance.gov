from django.http import Http404, HttpResponseRedirect

from v1.models import InternalDocsSettings


def redirect_to_internal_docs(request):
    docs_url = InternalDocsSettings.load(request_or_site=request).url

    if docs_url is None:
        raise Http404

    return HttpResponseRedirect(docs_url)
