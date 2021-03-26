# Debugging Templates

Module templates can be debugged visually through use of a `TemplateDebugView`
that renders a single module with a series of test cases.

Consider an example module that renders a simple hyperlink. This module
requires a target URL and also accepts optional link text. A simple Jinja
template for this module might look like this:

```html
<a href="{{ value.url }}">
    {{ value.text | default( value.url, true ) }}
</a>
```

## Defining template test cases

Next, define test cases for the module that cover all supported input
configurations. For this simple link module, there are only a few useful
test cases, but more complicated modules might have many more.

Test cases should be defined as a Python dict, where the key is a string name
of the test case and the value is a dict that will be passed to the module
template.

```py
# myapp/template_debug.py
link_test_cases = {
    'Link without text': {
        'url': 'https://www.consumerfinance.gov',
    },

    'Link with empty text': {
        'url': 'https://www.consumerfinance.gov',
        'text': '',
    },

    'Link with text': {
        'url': 'https://www.consumerfinance.gov',
        'text': 'Visit our website',
    },
}
```

## Registering the template debug view

The next step is to register the template debug view with Django so that it can
be loaded in a browser.

```py
# in myapp/wagtail_hooks.py
from myapp.template_debug import link_test_cases
from v1.template_debug import register_template_debug

register_template_debug('myapp', 'link', 'myapp/link.html', link_test_cases)
```

Once logged into the Wagtail admin, the template debug view for this module
will now be available at the `/admin/template_debug/myapp/link/` URL.

## Including component JavaScript

Associated JavaScript required by the module can be included in the template
debug view by listing it in the `register_template_debug` call:

```py
register_template_debug(
    'myapp',
    'link',
    'myapp/link.html',
    link_test_cases
    extra_js=['link.js']
)
```
