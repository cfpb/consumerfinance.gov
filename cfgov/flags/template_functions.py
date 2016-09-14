from django.core.exceptions import ObjectDoesNotExist
from wagtail.wagtailcore.models import Site

from flags.models import Flag


def flag_enabled(request, key):
    site = Site.find_for_request(request)

    try:
        return site.flag_states.get(flag_id=key).enabled
    except ObjectDoesNotExist:
        pass

    try:
        return Flag.objects.get(key=key).enabled_by_default
    except ObjectDoesNotExist:
        return False


def flags_enabled(request, *keys):
    return all(flag_enabled(request, key) for key in keys)


def flag_disabled(request, key):
    return not flag_enabled(request, key)
