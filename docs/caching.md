# Caching

### Akamai

We use [Akamai](https://www.akamai.com/), a content delivery network, to cache the entirety of [www.consumerfinance.gov](https://www.consumerfinance.gov/) (but not our development servers). We invalidate any given page in Wagtail when it is published or unpublished (by hooking up the custom class [`AkamaiBackend`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/models/akamai_backend.py) to [Wagtail's frontend cache invalidator](http://docs.wagtail.io/en/v2.0.1/reference/contrib/frontendcache.html). By default, we clear the Akamai cache any time we deploy.

There are certain pages that do not live in Wagtail or are impacted by changes on another page (imagine our [newsroom page](https://www.consumerfinance.gov/about-us/newsroom/) that lists titles of other pages) or another process (imagine data from Socrata gets updated) and thus will display outdated content until the page's time to live (TTL) has expired, a deploy has happened, or if someone manually invalidates that page. Our default TTL is 24 hours.

### Django caching

Starting in December 2017, we use [template fragment caching](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/v1/fragment_cache_extension.py) to cache all or part of a template.  It is enabled on our "post previews", snippets of a page that we display on results of filterable pages (e.g. [our blog page](https://consumerfinance.gov/about-us/blog) & [research & reports](https://www.consumerfinance.gov/data-research/research-reports/)).

It can easily be enabled on other templates. See [this PR](https://github.com/cfpb/cfgov-refresh/pull/3663/files) as an example of the code that would need to be introduced to cache a new fragment.

When a page gets published, it will update the post preview cache for that particular page.  However, if there are code changes that impact the page's content, or the post preview template itself gets updated, the entire post preview cache will need to be manually cleared. Clearing this particular cache could be an option when deploying, as it is with Akamai, but should not be a default since most deploys wouldn't impact the code in question.  Currently, the manual way to do this would be to run the following from a production server:

```
from django.core.cache import caches

caches['post_preview'].clear()
```

To run the application locally with caching for post previews enabled, run `ENABLE_POST_PREVIEW_CACHE=1 ./runserver.sh`
Alternatively, add this variable to your `.env` if you generally want it enabled locally.

Due to the impossibility/difficulty/complexity of caching individual Wagtail blocks (they are not serializable) and invalidating content that does not have some type of `post_save` hook (e.g. Taggit models), we have started with caching segments that are tied to a Wagtail page (which can be easily invalidated using the `page_published` Wagtail signal), hence the post previews. With more research or improvements to these third-party libraries, it is possible we could expand Django-level caching to more content.
