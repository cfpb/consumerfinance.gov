from django.urls import path

from . import views


app_name = "tccp"
urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("cards/", views.CardListView.as_view(), name="cards"),
    path(
        "cards/<slug:pk>/", views.CardDetailView.as_view(), name="card_detail"
    ),
]
