from django_filters.rest_framework import DjangoFilterBackend


class CardSurveyDataFilterBackend(DjangoFilterBackend):
    """Custom filter backend for card filtering.

    This backend passes summary statistics to the filterset.

    It also keeps a reference to its most recent filterset.
    """

    def __init__(self, summary_stats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_stats = summary_stats

    def get_filterset_kwargs(self, *args, **kwargs):
        kwargs = super().get_filterset_kwargs(*args, **kwargs)
        kwargs["summary_stats"] = self.summary_stats
        return kwargs

    def get_filterset(self, *args, **kwargs):
        self._used_filterset = super().get_filterset(*args, **kwargs)
        return self._used_filterset

    @property
    def used_filterset(self):
        return getattr(self, "_used_filterset", None)
