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

    def clean_q(self):
        return make_safe(self.cleaned_data["q"])
