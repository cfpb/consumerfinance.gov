from django.db import models


class Synonym(models.Model):
    synonym = models.CharField(
        max_length=500,
        help_text="A comma-separated list of words that are synonyms"
    )
