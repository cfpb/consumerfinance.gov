import datetime

from django.template import engines
from django.test import TestCase

from regulations3k.jinja2tags import ap_date, regs_hide_on_mobile


class RegulationsExtensionTestCase(TestCase):
    def test_ap_date(self):
        test_date = datetime.date(2011, 1, 1)
        result = ap_date(test_date)
        self.assertEqual(result, "Jan. 1, 2011")

    def test_ap_date_sept(self):
        test_date = datetime.date(2011, 9, 1)
        result = ap_date(test_date)
        self.assertEqual(result, "Sept. 1, 2011")

    def test_ap_date_march(self):
        test_date = datetime.date(2011, 3, 1)
        result = ap_date(test_date)
        self.assertEqual(result, "March 1, 2011")

    def test_ap_date_string(self):
        test_date = "2011-01-01"
        result = ap_date(test_date)
        self.assertEqual(result, "Jan. 1, 2011")

    def test_ap_date_invalid_string(self):
        test_date = "I am not a date"
        result = ap_date(test_date)
        self.assertEqual(result, None)

    def test_ap_date_none_date(self):
        result = ap_date(None)
        self.assertEqual(result, None)

    def test_regdown_filter_available(self):
        jinja2_engine = engines["wagtail-env"]
        template = jinja2_engine.from_string('{{ "*Hello*" | regdown }}')
        result = template.render()
        self.assertEqual(
            result,
            '<p class="regdown-block" data-label="" '
            'id="be34deef8eb9a480514ed3b4a5ebdaea61c711d2b11d40e830cb0656">'
            "<em>Hello</em></p>",
        )

    def test_regs_hide_on_mobile(self):
        test_str = "Regulation C"
        result = regs_hide_on_mobile(test_str)
        self.assertEqual(
            result, 'Reg<span class="u-hide-on-mobile">ulation</span> C'
        )
