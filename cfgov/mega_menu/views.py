from django.utils import translation

from wagtail.contrib.modeladmin.views import WMABaseView


class MenuPreviewView(WMABaseView):
    language = None

    def __init__(self, model_admin, language):
        super().__init__(model_admin)
        self.language = language

    def get_meta_title(self):
        return "Previewing %s %s" % (self.verbose_name, self.language)

    def get_template_names(self):
        return self.model_admin.get_preview_template()

    def render_to_response(self, context, **response_kwargs):
        translation.activate(self.language)
        self.request.LANGUAGE_CODE = translation.get_language()
        return super().render_to_response(context, **response_kwargs)
