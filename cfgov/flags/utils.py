from django.conf.urls import include

from .models import Flag, FlagState
from .template_functions import flag_enabled


def missing_flag_states_for_site(site, exclude_keys):
    return (FlagState(site=site, flag=f, enabled=f.enabled_by_default)
            for f in Flag.objects.exclude(key__in=exclude_keys))


def init_missing_flag_states_for_site(site):
    saved_states = site.flagstate_set.all()
    saved_keys = [ss.flag_id for ss in saved_states]
    missing_states = missing_flag_states_for_site(site, saved_keys)

    return [state.save() for state in missing_states]


def conditional_include(flag, *args, **kwargs):
    if flag_enabled(flag):
        return include(*args, **kwargs)
    else:
        return []
