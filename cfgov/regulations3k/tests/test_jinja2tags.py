from django.test import TestCase
from django.template import engines


class RegDownExtensionTestCase(TestCase):

    def test_regdown_filter_available(self):
        jinja2_engine = engines['wagtail-env']
        template = jinja2_engine.from_string('{{ "*Hello*" | regdown }}')
        result = template.render()
        self.assertEqual(
            result,
            '<p id="be34deef8eb9a480514ed3b4a5ebdaea61c711d2b11d40e830cb0656">'
            '<em>Hello</em></p>'
        )
