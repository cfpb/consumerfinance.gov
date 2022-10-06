from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class DataPoint(ClusterableModel):
    number = models.IntegerField(blank=True)
    title = models.CharField(max_length=400, blank=True)
    anchor = models.CharField(max_length=400, blank=True)
    rule_section = models.CharField(max_length=100, blank=True)
    intro_text = models.TextField(blank=True)
    page = ParentalKey(
        "FIGContentPage",
        on_delete=models.CASCADE,
        related_name="data_points",
        blank=True,
        null=True,
    )


class DataFieldJson(models.Model):
    info = models.JSONField(blank=True)
    data_point = ParentalKey(
        "DataPoint",
        on_delete=models.CASCADE,
        related_name="data_fields_json",
        blank=True,
        null=True,
    )
