from django.db import models


class Synonym(models.Model):
    synonym = models.CharField(max_length=500)
