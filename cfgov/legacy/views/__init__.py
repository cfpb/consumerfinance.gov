from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def token_provider(request):
    request.session.modified = True
    if request.method == 'POST':
        return render(request, 'common/csrf.html')
    return HttpResponse()
