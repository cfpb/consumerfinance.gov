import random

from django.template import engines
from django.test import TestCase

from agreements.models import Agreement, Issuer


class TestJinja2Tags(TestCase):
    def _render(self, s, context={}):
        template = engines["wagtail-env"].from_string(s)
        return template.render(context)

    def test_agreements_issuer_select(self):
        """Confirm that the agreements_issuer_select tag doesn't explode."""
        html = self._render("{{ agreements_issuer_select() | safe }}")
        self.assertIn("<select", html)

    def test_agreements_issuer_select_entries(self):
        """agreements_issuer_select tag should include all issuers."""
        names = [letter * 6 for letter in ["A", "B", "C", "D", "E"]]

        random_order_names = random.sample(names, len(names))
        for name in random_order_names:
            issuer = Issuer.objects.create(name=name, slug=name)
            Agreement.objects.create(issuer=issuer, size=1234)

        html = self._render("{{ agreements_issuer_select() | safe }}")

        for l_idx in range(len(names)):
            self.assertTrue(names[l_idx] in html)
            #   Also, verify that this letter comes before the others
            for r_idx in range(l_idx + 1, len(names)):
                self.assertTrue(
                    html.find(names[l_idx]) < html.find(names[r_idx])
                )

    def test_issuer_select_selected(self):
        """
        issuer_select tag should default to the selected id.
        """
        for name in ("AAA", "BBB", "CCC"):
            issuer = Issuer.objects.create(name=name, slug=name)
            Agreement.objects.create(issuer=issuer, size=1234)

        html = self._render(
            "{{ agreements_issuer_select(selected) | safe }}",
            {"selected": "BBB"},
        )

        self.assertInHTML('<option value="AAA">AAA</option>', html)
        self.assertInHTML('<option value="BBB" selected>BBB</option>', html)
        self.assertInHTML('<option value="CCC">CCC</option>', html)
