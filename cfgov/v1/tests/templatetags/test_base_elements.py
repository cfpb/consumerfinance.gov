from unittest import TestCase

from django.template import Context, Template
from django.test import RequestFactory


class TestHeaderFooter(TestCase):
    def setUp(self):
        request = RequestFactory().get("/")
        self.context = Context({"request": request})

    def test_render_header(self):
        tmpl = Template("{% load base_elements %}{% include_header %}")
        html = tmpl.render(self.context)
        self.assertIn('<header class="o-header">', html)

    def test_render_footer(self):
        tmpl = Template("{% load base_elements %}{% include_footer %}")
        html = tmpl.render(self.context)
        self.assertIn('<footer class="o-footer">', html)

    def test_render_modernizr(self):
        tmpl = Template("{% load base_elements %}{% include_modernizr %}")
        html = tmpl.render(self.context)
        self.assertIn("window.Modernizr", html)
