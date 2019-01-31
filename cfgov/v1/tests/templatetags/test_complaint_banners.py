from django.template import Context, Template
from django.test import RequestFactory, SimpleTestCase, override_settings


class TestComplaintIssueBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load complaint_banners %}'
            '{% complaint_issue_banner request %}'
        )
        return template.render(Context({'request': request}))

    def test_banner_renders(self):
        response = self.render('/some/other/path/')
        self.assertIn('m-global-banner', response)
