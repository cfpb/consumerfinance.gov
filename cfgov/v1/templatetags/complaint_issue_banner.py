from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def complaint_issue_banner(request):
    if request.path in settings.COMPLAINT_INTAKE_TECHNICAL_ISSUES_URLS:
        template = 'organisms/complaint-issue-banner.html'
        return mark_safe(render_to_string(template))

    return ''
