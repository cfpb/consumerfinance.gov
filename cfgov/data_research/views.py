from .forms import ConferenceRegistrationForm
from core.views import govdelivery_subscribe

@require_http_methods(['POST'])
def register(request):
    is_ajax = request.is_ajax()
    form = ConferenceRegistrationForm(request.POST)

    if form.is_valid():
        # do the registration and data save
        response = govdelivery_subscribe(request)
        if is_passing(response, is_ajax):
            form.save()
        return response
    else:
        # User does not have JS enabled AND the form is invalid
        # return failing response / redirect
        # TODO: Make our own server error that is applicable to "user submitted bad content w/o JS"
        page_id = request.get('page_id', None)
        if page_id:
            try:
                page = CFGOVPage.objects.get(id=page_id)
            except CFGOVPage.DoesNotExist:
                raise CFGOVPage.DoesNotExist
            # TODO: Figure out the least-bad way to notify the user this has failed (JS disabled)
            # page.serve(request,)
        return redirect('govdelivery:server_error')

def is_passing(response, is_ajax):
    if is_ajax:
        if 'pass' in response['result']:
            return True
    else:
        if 'success' in response.location:
            return True
    
    return False
