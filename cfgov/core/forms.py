import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.signing import Signer, BadSignature
from django.conf import settings

EXTERNAL_URL_WHITELIST_RAW = getattr(settings, 'EXTERNAL_URL_WHITELIST', ())
EXTERNAL_URL_WHITELIST = [re.compile(regex) for regex in EXTERNAL_URL_WHITELIST_RAW]

class ExternalURLForm(forms.Form):
    ext_url = forms.URLField(widget=forms.HiddenInput)
    signature = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(ExternalURLForm, self).clean()
        signer = Signer()

        if self.errors:
            # if it's not a valid URL, no reason to do further validation
            return

        url = cleaned_data['ext_url']
        matched_whitelist = any((regex.match(url) for regex in EXTERNAL_URL_WHITELIST))

        if matched_whitelist:
            cleaned_data['validated_url'] = url

        elif 'signature' in cleaned_data:
            signed_url = "{ext_url}:{signature}".format(**cleaned_data)
            try:
                cleaned_data['validated_url'] = signer.unsign(signed_url)
            except BadSignature:
                raise ValidationError(_('Signature validation failed'),
                                      code='invalid')
        else:
            raise ValidationError(_('URL must either be allowed by '
                                    'settings.EXTERNAL_URL_WHITELIST '
                                    'or have a valid signature'),
                                  code='invalid')
