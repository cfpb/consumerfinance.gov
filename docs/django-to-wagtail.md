# Wagtail pages vs. Django views

Rather than using “classic” Django views added to urls.py, when feasible an app should provide singleton Wagtail Page. This will allow site editors to drop that page anywhere in the site’s URL structure that they wish. A Wagtail Page subclass can do anything a Django view can [when overriding the serve method](http://docs.wagtail.io/en/v2.0.1/topics/pages.html#more-control-over-page-rendering).

```python
from django.http import HttpResponse
from wagtail.wagtailcore.models import Page,

class HelloWorldPage(CFGOVPage):
    def serve(self, request):
        return HttpResponse("Hello World")
```

By working with the Wagtail CMS, we also get some of the benefits of feature flags for free.
