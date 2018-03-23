"""Django-compatible widgets that render like Capital Framework.

See https://cfpb.github.io/capital-framework/components/cf-forms/ for
documentation on the styles that are being duplicated here.
"""
from __future__ import unicode_literals

from django.forms import widgets
from django.utils.html import format_html


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


class SubWidgetExtraAttrsMixin(object):
    """Mixin object to add extra attributes to a Django SubWidget."""
    extra_attrs = []

    def __init__(self, name, value, attrs, choice, index):
        attrs.update(self.extra_attrs)
        super(SubWidgetExtraAttrsMixin, self).__init__(
            name,
            value,
            attrs,
            choice,
            index
        )


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


class CheckboxChoiceInput(SubWidgetExtraAttrsMixin,
                          widgets.CheckboxChoiceInput):
    extra_attrs = [
        ('class', 'a-checkbox'),
    ]

    def render(self, name=None, value=None, attrs=None, choices=()):
        """Override the render function to add proper CF styling.

        By default Django renders checkbox choice inputs where the <label>
        tag wraps the <input> tag. Capital Framework instead specifies
        that the <input> tag come first, followed by the <label>.
        """
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''

        attrs = dict(self.attrs, **attrs) if attrs else self.attrs

        return format_html(
            (
                '<div class="m-form-field m-form-field__checkbox">'
                '{} <label class="a-label" {}>{}</label>'
                '</div>'
            ),
            self.tag(attrs),
            label_for,
            self.choice_label
        )


class CheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    """Custom renderer that outputs subwidgets with no wrapping.

    By default the renderer used to display checkbox choice inputs wraps the
    list in a <ul></ul> tag and wraps each element in <li><li>. Capital
    Framework specifies no such wrapping, so this class removes them.
    """
    choice_input_class = CheckboxChoiceInput
    outer_html = '{content}'
    inner_html = '{choice_value}{sub_widgets}'


class CheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    renderer = CheckboxFieldRenderer
