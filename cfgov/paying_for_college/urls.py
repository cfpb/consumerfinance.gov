from django.conf.urls import include, url


urlpatterns = [
    url(r'^understanding-your-financial-aid-offer/',
        include('paying_for_college.disclosures.urls',
                namespace='disclosures')),
]
