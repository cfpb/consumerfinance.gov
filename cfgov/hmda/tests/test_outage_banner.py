from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from flags.sources import get_flags


# Remove this file after the HMDA API is retired (hopefully summer 2019)
class TestHmdaOutageBannerTag(TestCase):
    outage_message = \
        'The HMDA Explorer tool and HMDA API have a planned outage today.'

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

    def test_banner_appears_when_flag_conditions_met(self):
        # test with any url in the /data-research category
        url = reverse('complaint-landing') + '?hmda-outage=True'
        response = self.client.get(url)
        self.assertContains(response, self.outage_message)

    def test_no_banner_when_param_not_true(self):
        url = reverse('complaint-landing') + '?hmda-outage=False'
        response = self.client.get(url)
        self.assertNotContains(response, self.outage_message)

    def test_no_banner_when_url_doesnt_match(self):
        url = reverse('fair-lending') + '?hmda-outage=True'
        response = self.client.get(url)
        self.assertNotContains(response, self.outage_message)
