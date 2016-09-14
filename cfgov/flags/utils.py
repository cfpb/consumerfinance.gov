from flags.models import Flag, FlagState


def init_missing_flag_states_for_site(site):
    existing_flags = site.flag_states.values_list('flag', flat=True)
    missing_flags = Flag.objects.exclude(key__in=existing_flags)

    FlagState.objects.bulk_create([
        FlagState(
            site=site,
            flag=flag,
            enabled=flag.enabled_by_default
        ) for flag in missing_flags
    ])
