from django import http
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def dbrouter_shortcut(request, content_type_id, object_id):
    """
    Redirect to an object's page based on a content-type ID and an object ID.
    """
    # Look up the object, making sure it's got a get_absolute_url() function.
    try:
        content_type = ContentType.objects.get(pk=content_type_id)
        if not content_type.model_class():
            raise http.Http404(
                _("Content type %(ct_id)s object has no associated model") %
                {'ct_id': content_type_id}
            )

        if content_type.app_label in settings.LEGACY_APPS:
            obj = content_type.model_class().objects.db_manager(
                'legacy').get(pk=object_id)
        else:
            obj = content_type.get_object_for_this_type(pk=object_id)

    except (ObjectDoesNotExist, ValueError):
        raise http.Http404(
            _("Content type %(ct_id)s object %(obj_id)s doesn't exist") %
            {'ct_id': content_type_id, 'obj_id': object_id}
        )

    try:
        get_absolute_url = obj.get_absolute_url
    except AttributeError:
        raise http.Http404(
            _("%(ct_name)s objects don't have a get_absolute_url() method") %
            {'ct_name': content_type.name}
        )

    return http.HttpResponseRedirect(get_absolute_url())


@csrf_exempt
def token_provider(request):
    request.session.modified = True
    if request.method == 'POST':
        context = RequestContext(request)
        return render_to_response('common/csrf.html', context)
    return HttpResponse()
