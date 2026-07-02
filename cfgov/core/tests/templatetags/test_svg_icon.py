from django.template import Context, Template
from django.test import TestCase


class SvgIconTests(TestCase):
    def test_template_tag(self):
        template = Template(
            '{% load svg_icon %}{% svg_icon "external-link" %}'
        )
        self.assertEqual(
            template.render(Context()),
            '<cfpb-icon name="external-link"></cfpb-icon>',
        )

    def test_template_tag_spin_attr(self):
        template = Template(
            '{% load svg_icon %}{% svg_icon "update" spin=True %}'
        )
        self.assertEqual(
            template.render(Context()),
            '<cfpb-icon name="update" spin></cfpb-icon>',
        )
