from django.template.response import TemplateResponse

from search import dotgov


def results_view(request):
    query = request.GET.get('q', '')

    results = dotgov.search(query)

    context = {
        'q': query,
        'results': results
    }

    response = TemplateResponse(request, 'search/results.html', context)
    return response.render()
