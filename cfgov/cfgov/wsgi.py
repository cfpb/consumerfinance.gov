"""
WSGI config for cfgov project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')


def initialize_new_relic():
    if os.getenv('NEW_RELIC_LICENSE_KEY'):
        new_relic_config_file = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../newrelic.ini'
            )
        )

        import newrelic.agent
        newrelic.agent.initialize(new_relic_config_file)


initialize_new_relic()

application = get_wsgi_application()
