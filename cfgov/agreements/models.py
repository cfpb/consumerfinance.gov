from django.db import models


class Issuer(models.Model):
    name = models.TextField(max_length=500)
    slug = models.TextField(max_length=500)


class Agreement(models.Model):
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    file_name = models.TextField(max_length=500)
    size = models.IntegerField()
    uri = models.URLField(max_length=500)
    description = models.TextField()
