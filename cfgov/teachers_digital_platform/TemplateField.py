from django.forms import Field

from .TemplateWidget import TemplateWidget


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
