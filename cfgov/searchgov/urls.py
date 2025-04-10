from django.urls import path

from . import views


app_name = "searchgov"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    #    path("api/", views.api, name="search_api"),
]
