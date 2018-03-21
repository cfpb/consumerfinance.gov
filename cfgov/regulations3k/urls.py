from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='regulations3k/base.html'),
        name='regulations_base'
    ),
]
