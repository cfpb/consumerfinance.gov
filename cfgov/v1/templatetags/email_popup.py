from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from flags.state import flag_enabled


register = template.Library()


@register.simple_tag
def email_popup(request):
    for label, details in settings.EMAIL_POPUP_URLS.items():
        for language, urls in details.items():
            if request.path not in urls:
                continue

            feature_flag = 'EMAIL_POPUP_{}'.format(label.upper())
            if not flag_enabled(feature_flag, request=request):
                continue

            template = 'organisms/email-popup/{}.html'.format(label)
            context = {'popup_label': label, 'popup_language': language}
            return mark_safe(render_to_string(template, context=context))

    return ''
