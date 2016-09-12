# Feature flags

Feature flags are stored in the Wagtail database and exposed in the Wagtail admin under “Settings”:

![Feature flags](img/image02.png)

Here flags can added, enabled, or disabled:

![Feature flags](img/image00.png)

The flag consists of a single string (by convention all uppercase, with underscores instead of whitespace). Flags are disabled by default, and checks for flags that do not exist will return False.

Once a flag has been created it can be checked in Python and Jinja2 templates using the functions `flag_enabled` and `flag_disabled` found in [`flags.template_functions`](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/flags/template_functions.py) and exposed to templates in v1. Checking the boolean value of a feature flag requires an `HttpRequest` object in order to determine the `Site` the flag is being checked against.

## Python example

```python
from flags.template_functions import flag_enabled, flag_disabled

if flag_enabled(request, 'BETA_NOTICE'):
	print(“Beta notice banner will be displayed”)

if flag_disabled(request, 'BETA_NOTICE'):
	print(“Beta notice banner will not be displayed”)
```

The `flags_enabled` method is also provided as a shortcut when checking that multiple flags are all set.

```python
from flags.template_functions import flags_enabled

if flags_enabled(request, 'FLAG1', 'FLAG2', 'FLAG3'):
	print(“All flags were set”)

```
	
## Jinja2 template example:

```
{% if flag_enabled(request, 'BETA_NOTICE') and show_banner %}
    <div class="m-global-banner">
I’m a beta banner.   
    </div>
{% endif %}
```

Feature flags are implemented as a Django app in [`cfgov-refresh/cfgov/flags`](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/flags).

## Feature flag hygiene

Feature flags should be rare and ephemeral. Changes should be small and frequent, and not big-bang releases, and flags that are no longer used should be cleaned up and removed from code and the database.

## Feature flag source

Feature flags for cfgov-refresh are implemented [in the `flags` Django app](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/flags).
