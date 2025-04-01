from operator import attrgetter
from urllib.parse import urlencode

from django.shortcuts import redirect, reverse
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from . import enums
from .filter_backend import CardSurveyDataFilterBackend
from .filterset import CardSurveyDataFilterSet
from .forms import LandingPageForm
from .jinja2tags import render_contact_info
from .models import CardSurveyData
from .serializers import CardSurveyDataListSerializer, CardSurveyDataSerializer
from .situations import Situation, SituationSpeedBumps


class LandingPageView(TemplateView):
    template_name = "tccp/landing_page.html"
    heading = "Explore credit cards for your situation"

    def get(self, request):
        form = LandingPageForm(request.GET)
        if form.is_valid():
            return self.redirect_to_results(**form.cleaned_data)

        return self.render_to_response(
            {
                "title": title(self.heading),
                "heading": self.heading,
                "form": LandingPageForm(),
                "stats": CardSurveyData.objects.get_summary_statistics(),
            }
        )

    def redirect_to_results(self, credit_tier, location, situations):
        return redirect(
            reverse("tccp:cards")
            + "?"
            + urlencode(
                {
                    "credit_tier": credit_tier,
                    "location": location,
                    "situations": list(map(attrgetter("title"), situations)),
                    **Situation.get_nonconflicting_params(situations),
                },
                doseq=True,
            )
        )


class AboutView(TemplateView):
    template_name = "tccp/about.html"
    breadcrumb_items = [
        {
            "title": "Credit cards",
            "href": "/consumer-tools/credit-cards/",
        },
        {
            "title": LandingPageView.heading,
            "href": reverse_lazy("tccp:landing_page"),
        },
    ]

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "breadcrumb_items": self.breadcrumb_items,
        }


class CardListView(ListAPIView):
    model = CardSurveyData
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = CardSurveyDataListSerializer
    filter_backends = [CardSurveyDataFilterBackend]
    filterset_class = CardSurveyDataFilterSet
    heading = "Explore credit cards"
    breadcrumb_items = [
        {
            "title": "Credit cards",
            "href": "/consumer-tools/credit-cards/",
        },
        {
            "title": LandingPageView.heading,
            "href": reverse_lazy("tccp:landing_page"),
        },
    ]

    def get_queryset(self):
        return self.model.objects.exclude_invalid_aprs()

    def get_template_names(self):
        if self.request.htmx:
            return ["tccp/includes/card_list.html"]
        else:
            return ["tccp/cards.html"]

    def list(self, request, *args, **kwargs):
        render_format = request.accepted_renderer.format

        queryset = self.get_queryset()
        summary_stats = queryset.get_summary_statistics()
        unfiltered_queryset = queryset.with_ratings(summary_stats)

        filter_backend = self.filter_backends[0]()

        try:
            filtered_queryset = filter_backend.filter_queryset(
                request, unfiltered_queryset, self
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
        cards = serializer.data

        response = Response(
            {
                "count": len(cards),
                "cards": cards,
                "stats_all": summary_stats,
            }
        )

        # If we're rendering HTML, we need to augment the response context.
        if render_format == "html":
            form = filter_backend.used_filterset.form
            situations = form.cleaned_data.get("situations", [])

            purchase_apr_rating_ranges = self.get_purchase_apr_rating_ranges(
                cards
            )

            response.data.update(
                {
                    "title": title(self.heading),
                    "heading": self.heading,
                    "breadcrumb_items": self.breadcrumb_items,
                    "form": form,
                    "situations": situations,
                    "speed_bumps": SituationSpeedBumps(situations),
                    "purchase_apr_rating_ranges": purchase_apr_rating_ranges,
                    "apr_rating_lookup": dict(enums.PurchaseAPRRatings),
                    "rewards_lookup": dict(enums.RewardsChoices),
                }
            )

        return response

    @classmethod
    def get_purchase_apr_rating_ranges(cls, cards):
        # In the ratings key we want to display a summary line like "Lower than
        # average (4.9% - 7.9%)". We've already computed the percentile cutoffs
        # for each rating but don't have the exact card APRs at the ends of
        # each rating. We could do this with another database query but the
        # size of the data is small enough to do it efficiently in Python.
        rating_ranges = {}

        for rating_score, _ in enums.PurchaseAPRRatings:
            # We use maximum APR here because that is what is used to assign
            # cards to rating groups.
            rating_maxes = [
                card["purchase_apr_for_tier_max"]
                for card in cards
                if card["purchase_apr_for_tier_rating"] == rating_score
            ]

            rating_ranges[rating_score] = (
                min(rating_maxes) if rating_maxes else None,
                max(rating_maxes) if rating_maxes else None,
            )

        return rating_ranges


class CardDetailView(RetrieveAPIView):
    model = CardSurveyData
    lookup_field = "slug"
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = CardSurveyDataSerializer
    template_name = "tccp/card.html"
    breadcrumb_items = CardListView.breadcrumb_items + [
        {
            "title": CardListView.heading,
            "href": reverse_lazy("tccp:cards"),
        }
    ]

    @cached_property
    def summary_stats(self):
        return (
            self.model.objects.exclude_invalid_aprs().get_summary_statistics()
        )

    def get_queryset(self):
        return self.model.objects.with_ratings(self.summary_stats)

    def retrieve(self, request, *args, **kwargs):
        card = self.get_object()
        serializer = self.get_serializer(card)

        response = Response(
            {
                "card": serializer.data,
                "stats_all": self.summary_stats,
            }
        )

        # If we're rendering HTML, we need to augment the response context.
        if request.accepted_renderer.format == "html":
            response.data.update(
                {
                    "breadcrumb_items": self.breadcrumb_items,
                    "credit_tier_lookup": enums.CreditTierConciseColumnChoices,
                    "apr_rating_lookup": dict(enums.PurchaseAPRRatings),
                    "state_lookup": dict(enums.StateChoices),
                    "rewards_lookup": dict(enums.RewardsChoices),
                    "render_contact_info": render_contact_info,
                }
            )

        return response

    def handle_exception(self, exc):
        """When rendering HTML, don't use DRF exception handling.

        The django-rest-framework package provides its own exception handling
        that includes HTML error templates, for example for 404 Not Found. We
        want to use our standard Django error templates even though this view
        is being served by DRF.

        If we're rendering JSON, we can use DRF's logic because it provides a
        nicer error message to the user.
        """
        if self.request.accepted_renderer.format == "html":
            raise exc

        return super().handle_exception(exc)
