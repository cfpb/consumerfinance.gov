from wagtail.wagtailcore import blocks

class ResearchConferenceRegistrationForm(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    days = blocks.ListBlock(blocks.CharBlock(label='Day'), label='Days attending')

    class Meta:
        icon = 'form'
        template = '_includes/research-conference-registration-form.html'
