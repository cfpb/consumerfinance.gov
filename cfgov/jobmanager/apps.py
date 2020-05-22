from django.apps import AppConfig


class JobManagerAppConfig(AppConfig):
    name = 'jobmanager'
    label = 'jobmanager'
    verbose_name = "Job Manager"

    def ready(self):
        from jobmanager.signals import register_signal_handlers
        register_signal_handlers()
