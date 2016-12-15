from django.conf.urls import url

from jobmanager.views import fellowship_form_submit


urlpatterns = [
    # Deprecated /jobs/design-technology-fellows/.
    # Will keep it to keep the external links functioning.
    url(r'^fellowship_form_submit/$',
        fellowship_form_submit,
        name='fellowship_form_submit'),
]
