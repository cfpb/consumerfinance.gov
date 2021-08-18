from django.forms.widgets import Input


class TemplateWidget(Input):
    """
    Widget that simply outputs a static template instead of an input.
    """
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
