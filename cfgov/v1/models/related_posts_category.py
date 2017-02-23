from v1.util import ref
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class RelatedPostsCategory(models.Model):
    name = models.CharField(max_length=255, choices=ref.categories)

    panels = [
        FieldPanel('name'),
    ]

    @classmethod
    def choices(cls):
        return [ 
            (category, category.name) for category in cls.objects.order_by('name')
        ]
