from django import forms


class RadioSelect(forms.RadioSelect):
    template_name = "tccp/widgets/radio.html"

    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs.setdefault("class", "a-radio")
        super().__init__(attrs=attrs, **kwargs)


class LandingPageRadioSelect(RadioSelect):
    option_template_name = "tccp/widgets/landing_page_radio_option.html"


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = "tccp/widgets/checkbox_option.html"

    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs.setdefault("class", "a-checkbox")
        super().__init__(attrs=attrs, **kwargs)


class Select(forms.Select):
    template_name = "tccp/widgets/select.html"
