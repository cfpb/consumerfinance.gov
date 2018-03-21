from django.conf.urls import url

from search.views import results_view


urlpatterns = [
    url(r'^$',
        results_view,
        # TemplateView.as_view(template_name='wellbeing/about.html')
        name='search_results'),
]
