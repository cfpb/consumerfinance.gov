from django.apps import AppConfig


class PayingForCollegeConfig(AppConfig):
    name = "paying_for_college"

    def ready(self):
        # Makes sure all signal handlers are connected
        from paying_for_college import handlers  # noqa
