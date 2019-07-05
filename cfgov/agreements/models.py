from django.db import models


class Issuer(models.Model):
    name = models.TextField(max_length=500)
    slug = models.TextField(max_length=500)


class Agreement(models.Model):
    issuer = models.ForeignKey(Issuer)
    file_name = models.TextField(max_length=500)
    size = models.IntegerField()
    uri = models.URLField(max_length=500)
    description = models.TextField()


class Prepaid(models.Model):
    name = models.CharField(blank=True, max_length=255)
    product_name = models.CharField(blank=True, max_length=255)
    other_relevant_parties = models.TextField(blank=True)
    status = models.TextField(blank=True)
    issuer = models.CharField(max_length=255, blank=True)
    issuer_name = models.CharField(max_length=255, blank=True)
    program_type = models.CharField(max_length=255, blank=True)
    withdrawal_date = models.DateField(blank=True, null=True)
    program_manager = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['product_name']


class Entity(models.Model):
    name = models.CharField(max_length=255, blank=True)
    salesforce_id = models.CharField(max_length=255, blank=True)
