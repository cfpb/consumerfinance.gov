# Debugging and Monitoring

### Using Django Debug Toolbar

When running locally it is possible to enable the
[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/)
by defining the `ENABLE_DEBUG_TOOLBAR` environment variable:

```sh
$ ENABLE_DEBUG_TOOLBAR=1 ./runserver.sh
```

This tool exposes various useful pieces of information about things like HTTP headers,
Django settings, SQL queries, and template variables. Note that running with the toolbar on
may have an impact on local server performance.

### Logging database queries to console

To log database queries to the console when running locally,
define the `ENABLE_SQL_LOGGING` environment variable:

```sh
$ ENABLE_SQL_LOGGING=1 cfgov/manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.count()
(0.004) SELECT COUNT(*) AS "__count" FROM "auth_user"; args=()
97
```

This will log any database queries (and time taken to execute them)
to the console, and works with any Django code invoked from the shell,
including the server and management commands:

```sh
$ ENABLE_SQL_LOGGING=1 ./runserver.sh
$ ENABLE_SQL_LOGGING=1 cfgov/manage.py some_management_command
```

### Logging Elasticsearch queries to console

Similarly, to log Elasticsearch queries to the console when running locally,
define the `ENABLE_ES_LOGGING` environment variable.

This will log any Elasticsearch queries (and time taken to execute them)
to the console, and works with any Django code invoked from the shell,
including the server and management commands:

```sh
$ ENABLE_ES_LOGGING=1 ./runserver.sh
$ ENABLE_ES_LOGGING=1 cfgov/manage.py some_management_command
```


### Monitoring using New Relic

This project can be configured for real-time monitoring with
[New Relic](https://newrelic.com/). This requires an active New Relic account
and a valid license key.

First, you'll need to install
[the New Relic Python Agent](https://docs.newrelic.com/docs/agents/python-agent)
from
[from PyPI](https://pypi.org/project/newrelic/).
This package is not part of the standard development requirements but is
included in
the [`requirements/deployment.txt`](https://github.com/cfpb/consumerfinance.gov/blob/main/requirements/deployment.txt) file.
It can be installed into your Python environment using the following command:

```shell
$ pip install newrelic
```

New Relic monitoring is implemented by wrapping every request to the Django
web server with a call to the Python agent. This agent records information
about web requests and reports it back to New Relic's servers. Additionally,
and depending on configuration, the agent also injects a bit of JavaScript
into every page header allowing for monitoring of client-side performance
in the web browser.

The New Relic Python agent has many
[configuration settings](https://docs.newrelic.com/docs/agents/python-agent/configuration/python-agent-configuration)
that control the information that gets recorded about web requests. This
project includes a default
[`newrelic.ini`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/newrelic.ini)
file that enables New Relic's
[high security mode](https://docs.newrelic.com/docs/agents/manage-apm-agents/configuration/high-security-mode)
to limit the recording of potentially sensitive information.

To activate New Relic monitoring of your instance of cf.gov, you'll need to set
two environment variables:

- `NEW_RELIC_LICENSE_KEY`: a valid New Relic license key
- `NEW_RELIC_APP_NAME`: a unique identifier to describe your running application

Make sure to choose a unique application name to help distinguish your web
traffic from any other users who may be running against the same New Relic
account.

This project's
[`.env_SAMPLE`](https://github.com/cfpb/consumerfinance.gov/blob/main/.env_SAMPLE)
file contains placeholder entries for these two variables.

Once you've set these two variables, start or restart your local web server.

When you make your first web request, you'll see messages in the console
indicating that the New Relic Python agent has been activated. You should also
see a message containing a link to the New Relic console:

```txt
Reporting to: https://rpm.newrelic.com/accounts/XXXXXXXX/applications/XXXXXXXX
```

You should now be able to use that link to navigate to the New Relic console
and, after a few seconds, see your web server traffic in New Relic APM and
New Relic Browser.
