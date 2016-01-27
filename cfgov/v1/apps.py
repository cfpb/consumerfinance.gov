from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .signals import user_save_callback

class V1AppConfig(AppConfig):
    name = 'v1'
    verbose_name = 'V1'

    def ready(self):
        user_model = get_user_model()
        post_save.connect(user_save_callback,sender=user_model)
