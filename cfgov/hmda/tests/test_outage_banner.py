from django.template import Context, Template
from django.test import RequestFactory, SimpleTestCase

from flags.sources import get_flags


class TestHmdaOutageBannerTag(SimpleTestCase):

    def render(self, path):
        request = RequestFactory().get(path)
        request.flag_conditions = get_flags()
        template = Template(
            '{% load hmda_banners %}'
            '{% hmda_outage_banner request %}'
        )
        return template.render(Context({'request': request}))

    def test_banner_renders(self):
        response = self.render('/data-research?hmda-outage=True')
        self.assertIn('m-global-banner', response)
