from .forms import ConferenceRegistrationForm
from core.views import govdelivery_subscribe

@require_http_methods(['POST'])
def register(request):
    is_ajax = request.is_ajax()
    context = {}
    form = ConferenceForm(request.POST)

    if form.is_valid():
        # do the registration and data save
        pass
    else:
        # return failing response
        # if the user doesn't have JS enabled then we need to handle it here
        return something