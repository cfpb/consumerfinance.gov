from django.urls import include, re_path


urlpatterns = [
    re_path(
        r"^understanding-your-financial-aid-offer/",
        include("paying_for_college.disclosures.urls"),
    ),
]
