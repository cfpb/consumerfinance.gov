"""Django-compatible widgets that render like Capital Framework.

See https://cfpb.github.io/capital-framework/components/cf-forms/ for
documentation on the styles that are being duplicated here.
"""
from __future__ import unicode_literals

from django.forms import widgets


class WidgetExtraAttrsMixin(object):
    """Mixin object to add extra attributes to a Django Widget.

    Also adds an additional `required` parameter that adds a `required`
    attribute to the widget. This is built-in behavior in Django 1.10+
    but is not yet available on Django 1.8.
    """
    extra_attrs = []

    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs.update(self.extra_attrs)

        if kwargs.pop('required', None):
            attrs['required'] = True

        super(WidgetExtraAttrsMixin, self).__init__(*args, **kwargs)


class TextInputAttrsMixin(WidgetExtraAttrsMixin):
    extra_attrs = [
        ('class', 'a-text-input a-text-input__full'),
    ]


class TextInput(TextInputAttrsMixin, widgets.TextInput):
    pass


class EmailInput(TextInputAttrsMixin, widgets.EmailInput):
    pass


class Textarea(TextInputAttrsMixin, widgets.Textarea):
    extra_attrs = TextInputAttrsMixin.extra_attrs + [
        ('rows', None),
        ('cols', None),
    ]
