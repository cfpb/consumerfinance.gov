from django.apps import AppConfig
from django.conf import settings


class SheerlikeConfig(AppConfig):
    name = 'sheerlike'
    verbose_name = 'Sheerlike'

    def ready(self):
        for app, directory in settings.SHEER_SITES.items():
            if directory.exists():
                engine_config = {
                    'NAME': app,
                    'BACKEND': 'django.template.backends.jinja2.Jinja2',
                    'DIRS': [
                        str(directory),
                        str(directory.child('_includes')),
                        str(directory.child('_layouts'))
                    ],
                    'OPTIONS': {
                        'environment': 'v1.environment',
                        'site_slug': app,
                    }
                }
                settings.TEMPLATES.append(engine_config)
