from django.db import models


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

    @property
    def latest_agreement(self):
        return self.prepaidagreement_set.order_by('-pk').first()

    class Meta:
        ordering = ['name']


class PrepaidAgreement(models.Model):
    product = models.ForeignKey(PrepaidProduct, on_delete=models.CASCADE)
    effective_date = models.DateField(blank=True, null=True)
    compressed_files_url = models.TextField(blank=True, null=True)
    bulk_download_path = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'IFL-' + str(self.pk)

    class Meta:
        ordering = ['-pk']
