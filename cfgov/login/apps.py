from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class LoginConfig(AppConfig):
    name = "login"

    def ready(self):
        from login.signals import user_save_callback

        user_model = get_user_model()
        post_save.connect(user_save_callback, sender=user_model)
