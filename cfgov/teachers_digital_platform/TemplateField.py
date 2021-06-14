from django.forms import Field
from django.forms.widgets import Input


_TPL_PREFIX = 'teachers_digital_platform/template-field/'


class TemplateWidget(Input):
    input_type = 'output'

    def __init__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        self.tpl = kwargs.pop('tpl')
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        html = self._render(f'{_TPL_PREFIX}{self.tpl}', context, renderer)
        html = f'<div class="tdp-TemplateWidget">{html}</div>'
        return html


class TemplateField(Field):
    '''
    Expects a template filename (inside /templates/teachers_digital_platform/template-field)

    E.g.  TemplateField('hello-world.html')
    '''
    widget = TemplateWidget

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        kwargs['disabled'] = True
        kwargs['label'] = ''
        tpl = args[0]
        args = args[1:]
        kwargs['widget'] = TemplateWidget(tpl=tpl)
        super().__init__(*args, **kwargs)
