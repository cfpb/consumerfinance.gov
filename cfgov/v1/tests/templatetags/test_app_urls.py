# -*- coding: utf-8 -*-
import six
from unittest import skipIf

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

    @skipIf(six.PY3, "Unicode workaround is unnecessary")
    def test_app_url_unicode(self):
        template = Template('{% load app_urls %}{% app_url request %}')
        request = RequestFactory().get('/äpp/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'pp')

    def test_app_page_url(self):
        template = Template('{% load app_urls %}{% app_page_url request %}')
        request = RequestFactory().get('/app/with/page/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'app/with/page/path')

    @skipIf(six.PY3, "Unicode workaround is unnecessary")
    def test_app_page_url_unicode(self):
        template = Template('{% load app_urls %}{% app_page_url request %}')
        request = RequestFactory().get('/ápp/with/päge/path')
        response = template.render(Context({'request': request}))
        self.assertEqual(response, 'pp/with/pge/path')
