from urllib.parse import urlencode

from django.db.models import Count, Min
from django.shortcuts import redirect, reverse
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

import django_filters.rest_framework
from flags.views import FlaggedTemplateView, FlaggedViewMixin
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .filterset import CardSurveyDataFilterSet
from .forms import LandingPageForm
from .models import CardSurveyData
from .serializers import CardSurveyDataSerializer


class LandingPageView(FlaggedTemplateView):
    flag_name = "TCCP"
    template_name = "tccp/landing_page.html"
    heading = "Explore credit cards for your situation"
    breadcrumb_items = [
        {
            "title": "Credit cards",
            "href": "/consumer-tools/credit-cards/",
        }
    ]

    def get(self, request):
        form = LandingPageForm(request.GET)
        if form.is_valid():
            return self.redirect_to_results(**form.cleaned_data)

        return self.render_to_response(
            {
                "title": title(self.heading),
                "heading": self.heading,
                "breadcrumb_items": self.breadcrumb_items,
                "form": LandingPageForm(),
                "num_cards": CardSurveyData.objects.count(),
            }
        )

    def redirect_to_results(self, credit_tier, situation):
        return redirect(
            reverse("tccp:cards")
            + "?"
            + urlencode(
                dict(targeted_credit_tiers=credit_tier, **situation.query)
            )
        )


class CardListView(FlaggedViewMixin, ListAPIView):
    flag_name = "TCCP"
    model = CardSurveyData
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = CardSurveyDataSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = CardSurveyDataFilterSet
    template_name = "tccp/cards.html"
    heading = "Customize for your situation"
    breadcrumb_items = LandingPageView.breadcrumb_items + [
        {
            "title": LandingPageView.heading,
            "href": reverse_lazy("tccp:landing_page"),
        }
    ]

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        render_format = request.accepted_renderer.format
        queryset = self.get_queryset()
        filter_backend = self.filter_backends[0]()

        try:
            filtered_queryset = filter_backend.filter_queryset(
                request, queryset, self
            )
        except ValidationError:
            # A ValidationError may occur if the user input is invalid.
            # If we're rendering JSON we can rely on django-rest-framework's
            # error handling.
            if render_format == "json":
                raise

            # If we're rendering HTML, we want to report the error to the
            # user, but we still need a queryset to render in the page.
            # We can use an empty queryset for this.
            filtered_queryset = self.model.objects.none()

        serializer = self.get_serializer(filtered_queryset, many=True)
        response = Response(
            {
                "count": len(serializer.data),
                "results": serializer.data,
            }
        )

        # If we're rendering HTML, we need to augment the response context.
        if render_format == "html":
            # We need a form object to render.
            filterset = filter_backend.get_filterset(
                request, filtered_queryset, self
            )

            # We also compute some statistics over the full dataset.
            statistics = queryset.aggregate(
                count=Count("pk"),
                first_report_date=Min("report_date"),
            )

            response.data.update(
                {
                    "title": title(self.heading),
                    "heading": self.heading,
                    "breadcrumb_items": self.breadcrumb_items,
                    "form": filterset.form,
                    "total_count": statistics["count"],
                    "first_report_date": statistics["first_report_date"],
                }
            )

        return response


class CardDetailView(FlaggedViewMixin, DetailView):
    flag_name = "TCCP"
    model = CardSurveyData
    context_object_name = "card"
    template_name = "tccp/card.html"
