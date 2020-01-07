# -*- coding: utf-8 -*-
import six
from unittest import skipUnless

from django.template import Context, Template
from django.test import RequestFactory, TestCase


class TestAppUrlTags(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_app_url(self):
        template = Template('{% load app_urls %}{% app_url request %}')
        request = RequestFactory().get('/app/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'app')

    @skipUnless(six.PY3, "Unicode in path doesn't work in python 2")
    def test_app_url_unicode(self):
        template = Template('{% load app_urls %}{% app_url request %}')
        request = RequestFactory().get('/äpp/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'äpp')

    def test_app_page_url(self):
        template = Template('{% load app_urls %}{% app_page_url request %}')
        request = RequestFactory().get('/app/with/page/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'app/with/page/path')

    @skipUnless(six.PY3, "Unicode in path doesn't work in python 2")
    def test_app_page_url_unicode(self):
        template = Template('{% load app_urls %}{% app_page_url request %}')
        request = RequestFactory().get('/ápp/with/päge/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'ápp/with/päge/path')
