from django_filters.rest_framework import DjangoFilterBackend


class CardSurveyDataFilterBackend(DjangoFilterBackend):
    """Custom filter backend for card filtering.

    This backend keeps a reference to its most recent filterset.
    """

    def get_filterset(self, *args, **kwargs):
        self._used_filterset = super().get_filterset(*args, **kwargs)
        return self._used_filterset

    @property
    def used_filterset(self):
        return getattr(self, "_used_filterset", None)
