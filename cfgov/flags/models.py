from django.db import models

from wagtail.wagtailcore.models import Site


class Flag(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.key

class FlagState(models.Model):
    flag = models.ForeignKey(Flag)
    site = models.ForeignKey(Site)
    enabled = models.BooleanField(default=False)
