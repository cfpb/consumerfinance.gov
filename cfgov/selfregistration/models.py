from django.db import models
from localflavor.us.models import USStateField, PhoneNumberField

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=1000)
    address1 =  models.CharField(max_length=1000)
    address2 =  models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=1000)
    state = USStateField()
    zip = models.CharField(max_length=5)
    tax_id = models.CharField(max_length = 100)
    website = models.URLField(blank=True, null=True)
    company_phone = PhoneNumberField()
    contact_name= models.CharField(max_length=1000)
    contact_title=  models.CharField(max_length = 100)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()
    contact_ext = models.CharField(max_length=50, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.company_name

    class Meta:
        ordering = ["submitted"]
        verbose_name_plural = "company info"

