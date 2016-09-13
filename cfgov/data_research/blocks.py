from wagtail.wagtailcore import blocks

class ConferenceRegistrationForm(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    code = blocks.CharBlock(required=True)
    sessions = blocks.ListBlock(blocks.CharBlock(label='Session'), label='Sessions attending')

    class Meta:
        icon = 'form'
        template = '_includes/research-conference-registration-form.html'
