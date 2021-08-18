from django.forms.widgets import RadioSelect


class ChoiceWidget(RadioSelect):
    """
    Subclass of Django's RadioSelect that allows passing in an opts_list to
    be rendered above the options.
    """
    input_type = 'radio'
    template_name = 'teachers_digital_platform/choice.html'

    def __init__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        self.opts_list = kwargs.pop('opts_list')
        super().__init__(*args, **kwargs)

    def get_context(self, *args):
        context = super().get_context(*args)
        context['opts_list'] = self.opts_list
        return context
