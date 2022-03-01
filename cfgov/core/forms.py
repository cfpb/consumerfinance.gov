import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, Signer
from django.utils.translation import gettext_lazy as _


EXTERNAL_URL_ALLOWLIST_RAW = getattr(settings, "EXTERNAL_URL_ALLOWLIST", ())
EXTERNAL_URL_ALLOWLIST = [
    re.compile(regex) for regex in EXTERNAL_URL_ALLOWLIST_RAW
]


class ExternalURLForm(forms.Form):
    ext_url = forms.URLField(widget=forms.HiddenInput)
    signature = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()
        signer = Signer()

        if self.errors:
            # if it's not a valid URL, no reason to do further validation
            return

        url = cleaned_data["ext_url"]
        matched_whitelist = any(
            (regex.match(url) for regex in EXTERNAL_URL_ALLOWLIST)
        )

        if matched_whitelist:
            cleaned_data["validated_url"] = url

        elif cleaned_data.get("signature"):
            signed_url = "{ext_url}:{signature}".format(**cleaned_data)
            try:
                cleaned_data["validated_url"] = signer.unsign(signed_url)
            except BadSignature:
                raise ValidationError(
                    _("Signature validation failed"), code="invalid"
                )
        else:
            raise ValidationError(
                _(
                    "URL must either be allowed by "
                    "settings.EXTERNAL_URL_ALLOWLIST "
                    "or have a valid signature"
                ),
                code="invalid",
            )
