from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.models import Site

from sheerlike.middleware import get_request

from .models import Flag

def flag_enabled(key):
    request = get_request()
    if not request:
        return False
    site = Site.find_for_request(request)
    state_for_site = site.flagstate_set.filter(flag_id=key, \
            ).first()
    if state_for_site is not None:
        return state_for_site.enabled

    else:
        try:
            flag = Flag.objects.get(pk=key)
            return flag.enabled_by_default
        except ObjectDoesNotExist:
            return False

def flag_disabled(key):
    return not flag_enabled(key)
