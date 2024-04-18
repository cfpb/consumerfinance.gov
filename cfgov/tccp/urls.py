from django.urls import path

from . import views


app_name = "tccp"
urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("cards/", views.CardListView.as_view(), name="cards"),
    path(
        "cards/<slug:slug>/",
        views.CardDetailView.as_view(),
        name="card_detail",
    ),
]
