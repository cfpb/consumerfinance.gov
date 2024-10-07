from django.apps import AppConfig

from wagtail.users.apps import WagtailUsersAppConfig

from . import checks  # noqa F401


class LoginConfig(AppConfig):
    name = "login"


class LoginUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "login.viewsets.UserViewSet"
