from django import http
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def token_provider(request):
    request.session.modified = True
    if request.method == 'POST':
        context = RequestContext(request)
        return render_to_response('common/csrf.html', context)
    return HttpResponse()
