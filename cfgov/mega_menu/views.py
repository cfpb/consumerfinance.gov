from django.utils import translation
from django.utils.functional import cached_property

from wagtail.contrib.modeladmin.views import EditView, WMABaseView


class MenuEditView(EditView):
    @cached_property
    def preview_url(self):
        return self.url_helper.get_action_url('preview', self.pk_quoted)


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
