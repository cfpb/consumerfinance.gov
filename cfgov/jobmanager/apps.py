from django.apps import AppConfig


class JobManagerAppConfig(AppConfig):
    name = 'jobmanager'
    label = 'jobmanager'
    verbose_name = "Job Manager"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from jobmanager.signals import register_signal_handlers
        register_signal_handlers()
