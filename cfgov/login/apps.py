from django.apps import AppConfig

from . import checks  # noqa F401


class LoginConfig(AppConfig):
    name = "login"
