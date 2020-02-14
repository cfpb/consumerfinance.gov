from django import template
from django.template.loader import render_to_string
from django.utils import dateparse, timezone
from django.utils.dateformat import format
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def collect_outage_banner(request):
    template = 'organisms/collect-outage-banner.html'
    return mark_safe(render_to_string(template))


@register.simple_tag
def complaint_issue_banner(request):
    template = 'organisms/complaint-issue-banner.html'
    return mark_safe(render_to_string(template))


@register.simple_tag
def complaint_maintenance_banner(request):
    """ Add a complaint maintenance banner.
    This banner is intended to be used along with the
    COMPLAINT_INTAKE_MAINTENANCE feature flag with a pair of 'after date' and
    'before date' conditions to indicate the maintenance window. The
    'before date' condition will be used to inform visitors when the
    maintenance window ends. """

    template = 'organisms/complaint-maintenance-banner.html'

    now = timezone.localtime()

    date_str = 'soon'

    # Get the date range from feature flag conditions
    maintenance_flag = getattr(
        request, 'flag_conditions', {}
    ).get(
        'COMPLAINT_INTAKE_MAINTENANCE'
    )

    # Get the 'before_date' condition (if one exists) and use it to make a date
    # string for the banner.
    if maintenance_flag is not None:
        before_dates = [
            c.value for c in maintenance_flag.conditions
            if c.condition == 'before date'
        ]
        for before_date in before_dates:
            try:
                before_date = dateparse.parse_datetime(before_dates[0])
            except TypeError:
                before_date = before_dates[0]

            before_date = timezone.localtime(before_date)

            if before_date > now:
                date_str = 'after {time} on {date}'.format(
                    time=format(before_date, 'g:i a e'),
                    date=format(before_date, 'l, F j, Y,'),
                )
                break

    context = {
        'date_str': date_str,
    }
    return mark_safe(render_to_string(template, context=context))


@register.simple_tag
def omwi_salesforce_outage_banner(request):
    template = 'organisms/omwi-salesforce-outage-banner.html'
    return mark_safe(render_to_string(template))
