from django.http import JsonResponse
import datetime


def search(request):
    now = datetime.datetime.now()
    results = {'search': {'timestamp': '%s' % now}}
    return JsonResponse(results)


def export(request):
    now = datetime.datetime.now()
    results = {'export': {'timestamp': '%s' % now}}
    return JsonResponse(results)


def suggest(request):
    now = datetime.datetime.now()
    results = {'suggest': {'timestamp': '%s' % now}}
    return JsonResponse(results)


def document(request, id):
    now = datetime.datetime.now()
    results = {'document': {'timestamp': '%s' % now, 'id': id}}
    return JsonResponse(results)
