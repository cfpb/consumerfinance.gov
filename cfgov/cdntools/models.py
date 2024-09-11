from django.contrib.auth.models import User
from django.db import models


class CDNHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=2083)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "v1_cdnhistory"
