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


class PrepaidProduct(models.Model):
    name = models.CharField(blank=True, max_length=255)
    issuer_name = models.CharField(max_length=255, blank=True)
    prepaid_type = models.CharField(max_length=255, blank=True, null=True)
    program_manager = models.CharField(max_length=255, blank=True, null=True)
    other_relevant_parties = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    withdrawal_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PrepaidAgreement(models.Model):
    product = models.ForeignKey(PrepaidProduct, on_delete=models.CASCADE)
    effective_date = models.DateField(blank=True, null=True)
    agreements_files_location = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.agreements_files_location
