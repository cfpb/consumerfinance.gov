from django.db import models
from wagtail.wagtailcore.models import Site


class Flag(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    enabled_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.key


class FlagState(models.Model):
    flag = models.ForeignKey(Flag, related_name='states')
    site = models.ForeignKey(Site, related_name='flag_states')
    enabled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('flag', 'site')
