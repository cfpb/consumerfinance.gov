from django.apps import AppConfig
from django.conf import settings


sheer_override_dir = settings.PROJECT_ROOT.child('jinja2', 'sheer_override')
common_overrides = sheer_override_dir.child('common')

class SheerlikeConfig(AppConfig):
    name = 'sheerlike'
    verbose_name = 'Sheerlike'

    def ready(self):
        for app, directory in settings.SHEER_SITES.items():
            if directory.exists():
                app_overrides =sheer_override_dir.child('app')
                engine_config = {
                    'NAME': app, 'BACKEND': 'django.template.backends.jinja2.Jinja2', 'DIRS': [
                        str(app_overrides),
                        str(common_overrides),
                        str(directory), str(
                            directory.child('_includes')), str(
                            directory.child('_layouts'))], 'OPTIONS': {
                        'environment': 'v1.environment', 'site_slug': app,
                        'extensions': [
                            'wagtail.wagtailcore.jinja2tags.core',
                            'wagtail.wagtailadmin.jinja2tags.userbar',
                            'wagtail.wagtailimages.jinja2tags.images',
                             ], }}
                settings.TEMPLATES.append(engine_config)
