from django.db import models


class PrepaidProduct(models.Model):
    name = models.CharField(blank=True, max_length=255)
    issuer_name = models.CharField(max_length=255, blank=True)
    prepaid_type = models.CharField(max_length=255, blank=True, null=True)
    program_manager = models.CharField(max_length=255, blank=True, null=True)
    program_manager_exists = models.CharField(
        max_length=255, blank=True, null=True)
    other_relevant_parties = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    withdrawal_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def most_recent_agreement(self):
        """ Gets most recent agreement, as determined by its created time."""
        return self.agreements.first()

    class Meta:
        ordering = ['name']


class PrepaidAgreement(models.Model):
    product = models.ForeignKey(
        PrepaidProduct, related_name='agreements', on_delete=models.CASCADE)
    created_time = models.DateTimeField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    compressed_files_url = models.TextField(blank=True, null=True)
    bulk_download_path = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    @property
    def is_most_recent(self):
        return self == self.product.most_recent_agreement

    class Meta:
        ordering = ['-created_time']
