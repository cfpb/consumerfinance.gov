from django.http import JsonResponse
import datetime
import complaint_search


def search(request):
    now = datetime.datetime.now()
    results = {'search': {'timestamp': '%s' % now}}
    results = complaint_search.search()
    return JsonResponse(results)


def suggest(request):
    now = datetime.datetime.now()
    results = {'suggest': {'timestamp': '%s' % now}}
    results = complaint_search.suggest()
    return JsonResponse(results)


def document(request, id):
    now = datetime.datetime.now()
    results = {'document': {'timestamp': '%s' % now, 'id': id}}
    results = complaint_search.document(id)
    return JsonResponse(results)
