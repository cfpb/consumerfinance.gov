from django_filters.rest_framework import DjangoFilterBackend


class StatsProvidingDjangoFilterBackend(DjangoFilterBackend):
    """Filter backend that passes summary statistics to the filterset."""

    def __init__(self, summary_stats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary_stats = summary_stats

    def get_filterset_kwargs(self, *args, **kwargs):
        kwargs = super().get_filterset_kwargs(*args, **kwargs)
        kwargs["summary_stats"] = self.summary_stats
        return kwargs
