from django import forms


MAX_CHARS = 75

UNSAFE_CHARACTERS = [
    "#",
    "%",
    ";",
    "^",
    "~",
    "`",
    "|",
    "<",
    ">",
    "[",
    "]",
    "{",
    "}",
    "\\",
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, "")
    return term[:MAX_CHARS]


class SearchForm(forms.Form):
    q = forms.CharField(strip=True)
    page = forms.IntegerField(required=False)

    def clean_q(self):
        return make_safe(self.cleaned_data["q"])

    def clean_page(self):
        raw = self.cleaned_data["page"]
        if raw is None:
            return 1
        try:
            return int(raw)
        except ValueError:
            return 1
