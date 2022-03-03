# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from django.http import HttpRequest, QueryDict
from django.template import engines
from django.test import TestCase


class TestPrepaidJinja2Tags(TestCase):
    def _render(self, s, context=None):
        if not context:
            context = {}
        template = engines["wagtail-env"].from_string(s)
        return template.render(context)

    def test_parameter_is_removed_from_querystring(self):
        request = HttpRequest()
        request.GET.update(QueryDict("a=1&b=2"))
        html = self._render(
            "{{ remove_url_parameter( request, params ) }}",
            {"request": request, "params": {"a": ["1"]}},
        )
        self.assertEqual("?b=2", html)

    def test_one_of_multiple_parameters_is_removed_from_querystring(self):
        request = HttpRequest()
        request.GET.update(QueryDict("a=1&a=2"))
        html = self._render(
            "{{ remove_url_parameter( request, params ) }}",
            {"request": request, "params": {"a": ["2"]}},
        )
        self.assertEqual("?a=1", html)

    def test_multiple_parameters_are_removed_from_querystring(self):
        request = HttpRequest()
        request.GET.update(QueryDict("a=1&a=2&b=3"))
        html = self._render(
            "{{ remove_url_parameter( request, params ) }}",
            {"request": request, "params": {"a": ["1", "2"]}},
        )
        self.assertEqual("?b=3", html)

    def test_original_querystring_returned_if_param_not_present(self):
        request = HttpRequest()
        request.GET.update(QueryDict("a=1"))
        html = self._render(
            "{{ remove_url_parameter( request, params ) }}",
            {"request": request, "params": {"a": ["2"]}},
        )
        self.assertEqual("?a=1", html)

    def test_unicode_params_are_correctly_encoded(self):
        request = HttpRequest()
        request.GET.update(QueryDict("a=1&a=unicodë"))
        html = self._render(
            "{{ remove_url_parameter( request, params ) }}",
            {"request": request, "params": {"a": ["1"]}},
        )
        self.assertEqual("?" + urlencode({"a": "unicodë"}, "utf-8"), html)
