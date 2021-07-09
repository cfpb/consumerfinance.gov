from django.forms import Field
from django.forms.widgets import Input


class TemplateWidget(Input):
    tpl_prefix = 'teachers_digital_platform/template-field/'
    input_type = 'output'

    def __init__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        self.tpl = kwargs.pop('tpl')
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        html = self._render(f'{self.tpl_prefix}{self.tpl}', context, renderer)
        html = f'<div class="tdp-TemplateWidget">{html}</div>'
        return html


class TemplateField(Field):
    """
    Field that simply renders a given template. The template name is prepended
    with TemplateWidget.tpl_prefix (
    default "teachers_digital_platform/template-field/")

    E.g. TemplateField('hello-world.html') will render the template
         "teachers_digital_platform/template-field/hello-world.html"
    """
    widget = TemplateWidget

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        kwargs['disabled'] = True
        kwargs['label'] = ''
        tpl = args[0]
        args = args[1:]
        kwargs['widget'] = TemplateWidget(tpl=tpl)
        super().__init__(*args, **kwargs)
