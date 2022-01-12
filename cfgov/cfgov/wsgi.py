"""
WSGI config for cfgov project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
import pathlib


def activate_venv():
    cfgov_current_path = pathlib.Path(os.getenv('CFGOV_CURRENT'))
    venv_path = cfgov_current_path / 'venv'
    if venv_path.exists():
        python_home = venv_path
        activate_this = python_home / 'bin/activate_this.py'
        exec(activate_this, dict(__file__=activate_this))


def initialize_new_relic():
    if os.getenv('NEW_RELIC_LICENSE_KEY'):
        new_relic_config_file = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '../newrelic.ini'
            )
        )

        import newrelic.agent
        newrelic.agent.initialize(new_relic_config_file)


activate_venv()
initialize_new_relic()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')

# We don't want to import this module until after initializing New Relic.
from django.core.wsgi import get_wsgi_application  # noqa: E402, isort:skip
application = get_wsgi_application()
