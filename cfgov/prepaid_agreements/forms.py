from django import forms


class SearchForm(forms.Form):
    """Django form to validate the basic prepaid search fields"""

    page = forms.IntegerField(required=False)
    q = forms.CharField(required=False)
    search_field = forms.ChoiceField(
        choices=[
            ("all", "All fields"),
            ("name", "Product name"),
            ("program_manager", "Program manager"),
            ("other_relevant_parties", "Other relevant party"),
        ],
        required=False,
    )


class FilterForm(forms.Form):
    """Django form to validate the prepaid search filter fields"""

    issuer_name = forms.MultipleChoiceField(choices=[], required=False)
    prepaid_type = forms.MultipleChoiceField(choices=[], required=False)
    status = forms.MultipleChoiceField(choices=[], required=False)

    def set_issuer_name_choices(self, choices):
        self.fields["issuer_name"].choices = [(c, c) for c in choices]

    def set_prepaid_type_choices(self, choices):
        self.fields["prepaid_type"].choices = [(c, c) for c in choices]

    def set_status_choices(self, choices):
        self.fields["status"].choices = [(c, c) for c in choices]
