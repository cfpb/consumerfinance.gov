from django.db import models

from tccp.fields import JSONListField


YEAR_IN_SCHOOL_CHOICES = [
    ("FR", "Freshman"),
    ("SO", "Sophomore"),
    ("JR", "Junior"),
    ("SR", "Senior"),
    ("GR", "Graduate"),
]


class NullableYearsInSchool(models.Model):
    years = JSONListField(
        choices=YEAR_IN_SCHOOL_CHOICES, null=True, blank=True
    )


class YearsInSchool(models.Model):
    years = JSONListField(choices=YEAR_IN_SCHOOL_CHOICES, blank=True)
