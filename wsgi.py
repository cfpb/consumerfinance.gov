"""
WSGI config for cfgov project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys


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

path = "/src/cfgov-refresh/cfgov"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')


# We don't want to import this module until after initializing New Relic.
from django.core.wsgi import get_wsgi_application  # noqa: E402, isort:skip
application = get_wsgi_application()
