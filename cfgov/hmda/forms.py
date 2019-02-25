from django import forms
from django.forms import widgets

HMDA_YEARS = (
    ('2017', '2017'),
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
    ('2009', '2009'),
    ('2008', '2008'),
    ('2007', '2007'),
)

HMDA_STATES = (
    ('AK', 'Alaska'),
    ('AL', 'Alabama'),
    ('AR', 'Arkansas'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('IA', 'Iowa'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('MA', 'Massachusetts'),
    ('MD', 'Maryland'),
    ('ME', 'Maine'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MO', 'Missouri'),
    ('MP', 'Northern Mariana Islands'),
    ('MS', 'Mississippi'),
    ('MT', 'Montana'),
    ('NA', 'National'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('NE', 'Nebraska'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NV', 'Nevada'),
    ('NY', 'New York'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VA', 'Virginia'),
    ('VI', 'Virgin Islands'),
    ('VT', 'Vermont'),
    ('WA', 'Washington'),
    ('WI', 'Wisconsin'),
    ('WV', 'West Virginia'),
    ('WY', 'Wyoming')
)

HMDA_ACTIONS = (
    ('all', 'All records'),
    ('originated', 'All originated mortgages'),
)


class HmdaFilterableForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HmdaFilterableForm, self).__init__(*args, **kwargs)

    years = forms.MultipleChoiceField(
        required=False,
        choices=HMDA_YEARS,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_year',
            'class': 'o-multiselect',
            'data-placeholder': 'Year',
            'multiple': 'multiple',
        })
    )

    states = forms.MultipleChoiceField(
        required=False,
        choices=HMDA_STATES,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_state',
            'class': 'o-multiselect',
            'data-placeholder': 'U.S. State',
            'multiple': 'multiple',
        })
    )

    action = forms.ChoiceField(
        required=False,
        choices=HMDA_ACTIONS,
        widget=widgets.RadioSelect(attrs={
            'id': 'o-hmda_actions',
            'class': 'o-hmda_actions',
            'data-placeholder': 'Mortgage action',
        })
    )
