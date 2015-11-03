from wagtail.wagtailcore.models import Site

from sheerlike.middleware import get_request

def flag_enabled(key):
    request = get_request()
    site = Site.find_for_request(request)
    return bool(site.flagstate_set.filter(flag_id=key, enabled=True).first())

def flag_disabled(key):
    return not flag_enabled(key)

