from django import forms


class RadioSelect(forms.RadioSelect):
    template_name = "tccp/widgets/radio.html"

    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs.setdefault("class", "a-radio")
        super().__init__(attrs=attrs, **kwargs)


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "tccp/widgets/checkbox_select.html"
    option_template_name = "tccp/widgets/checkbox_option.html"

    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs.setdefault("class", "a-checkbox")
        super().__init__(attrs=attrs, **kwargs)


class SituationSelectMultiple(CheckboxSelectMultiple):
    option_template_name = "tccp/widgets/situation_checkbox_option.html"


class Select(forms.Select):
    template_name = "tccp/widgets/select.html"


class OrderingSelect(Select):
    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs.setdefault("form", "tccp-filters")
        super().__init__(attrs=attrs, **kwargs)
