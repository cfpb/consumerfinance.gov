from operator import attrgetter
from urllib.parse import urlencode

from django.shortcuts import redirect, reverse
from django.template.defaultfilters import title
from django.urls import reverse_lazy

from flags.views import FlaggedTemplateView, FlaggedViewMixin
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .enums import RewardsChoices, StateChoices
from .filter_backend import CardSurveyDataFilterBackend
from .filterset import CardSurveyDataFilterSet
from .forms import LandingPageForm
from .models import CardSurveyData
from .serializers import CardSurveyDataListSerializer, CardSurveyDataSerializer
from .situations import Situation


class LandingPageView(FlaggedTemplateView):
    flag_name = "TCCP"
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


class CardListView(FlaggedViewMixin, ListAPIView):
    flag_name = "TCCP"
    model = CardSurveyData
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = CardSurveyDataListSerializer
    filter_backends = [CardSurveyDataFilterBackend]
    filterset_class = CardSurveyDataFilterSet
    heading = "Customize for your situation"
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
        return self.model.objects.all()

    def get_template_names(self):
        if self.request.htmx:
            return ["tccp/includes/card_list.html"]
        else:
            return ["tccp/cards.html"]

    def list(self, request, *args, **kwargs):
        render_format = request.accepted_renderer.format
        queryset = self.get_queryset()
        summary_stats = queryset.get_summary_statistics()
        filter_backend = self.filter_backends[0](summary_stats)

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
                "stats_all": summary_stats,
            }
        )

        # If we're rendering HTML, we need to augment the response context.
        if render_format == "html":
            response.data.update(
                {
                    "title": title(self.heading),
                    "heading": self.heading,
                    "breadcrumb_items": self.breadcrumb_items,
                    "form": filter_backend.used_filterset.form,
                    "rewards_lookup": dict(RewardsChoices),
                }
            )

        return response


class CardDetailView(FlaggedViewMixin, RetrieveAPIView):
    flag_name = "TCCP"
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

    def get_queryset(self):
        return self.model.objects.all()

    def retrieve(self, request, *args, **kwargs):
        card = self.get_object()
        serializer = self.get_serializer(card)

        # If we're rendering HTML, we need to augment the response context.
        if request.accepted_renderer.format == "html":
            response = Response(
                {
                    "card": serializer.data,
                    "breadcrumb_items": self.breadcrumb_items,
                    "state_lookup": dict(StateChoices),
                    "rewards_lookup": dict(RewardsChoices),
                }
            )
        else:
            response = Response(serializer.data)

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
