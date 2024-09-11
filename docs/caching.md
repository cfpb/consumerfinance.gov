# Caching

### Akamai

We use [Akamai](https://www.akamai.com/), a content delivery network, to cache the entirety of [www.consumerfinance.gov](https://www.consumerfinance.gov/) (but not our development servers). We invalidate any given page in Wagtail when it is published or unpublished (by hooking up the custom class [`AkamaiBackend`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/cdntools/backends.py) to [Wagtail's frontend cache invalidator](http://docs.wagtail.io/en/v2.0.1/reference/contrib/frontendcache.html).

There are certain pages that do not live in Wagtail or are impacted by changes on another page (imagine our [newsroom page](https://www.consumerfinance.gov/about-us/newsroom/) that lists titles of other pages) or another process (imagine data from Socrata gets updated) and thus will display outdated content until the page's time to live (TTL) has expired, a deploy has happened, or if someone manually invalidates that page. Our default TTL is 24 hours.

#### Checking the cache state of a URL

To get the current cache state of a URL (perhaps to see if that URL has been invalidated), you can use the following `curl` command to check the `X-Cache` header:

```shell
curl -sI -H "Pragma: akamai-x-cache-on" https://beta.consumerfinance.gov | grep "X-Cache"
```

It will return something like:

```
X-Cache: TCP_HIT from a23-46-239-53.deploy.akamaitechnologies.com (AkamaiGHost/9.5.4-24580776) (-)
```

The possible cache state values are:

- `TCP_HIT`: The object was fresh in cache and object from disk cache.
- `TCP_MISS`: The object was not in cache, server fetched object from origin.
- `TCP_REFRESH_HIT`: The object was stale in cache and we successfully refreshed with the origin on an If-modified-Since request.
- `TCP_REFRESH_MISS`: Object was stale in cache and refresh obtained a new object from origin in response to our IF-Modified-Since request.
- `TCP_REFRESH_FAIL_HIT`: Object was stale in cache and we failed on refresh (couldn't reach origin) so we served the stale object.
- `TCP_IMS_HIT`: IF-Modified-Since request from client and object was fresh in cache and served.
- `TCP_NEGATIVE_HIT`: Object previously returned a "not found" (or any other negatively cacheable response) and that cached response was a hit for this new request.
- `TCP_MEM_HIT`: Object was on disk and in the memory cache. Server served it without hitting the disk.
- `TCP_DENIED`: Denied access to the client for whatever reason.
- `TCP_COOKIE_DENY`: Denied access on cookie authentication (if centralized or decentralized authorization feature is being used in config).
