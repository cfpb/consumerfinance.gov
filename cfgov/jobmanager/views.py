from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from jobmanager.models import FellowshipUpdateList


@csrf_exempt
def fellowship_form_submit(request):
    if request.POST:
        P = request.POST
        FellowshipUpdateList(
            email=P.get('email'),
            first_name=P.get('first_name'),
            last_name=P.get('last_name'),
            likes_design=bool(P.get('likes_design', False)),
            likes_cybersecurity=bool(P.get('likes_cybersecurity', False)),
            likes_development=bool(P.get('likes_development', False)),
            likes_data=bool(P.get('likes_data', False)),
        ).save()

    return HttpResponse('OK')
