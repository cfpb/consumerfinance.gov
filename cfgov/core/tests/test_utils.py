from django.template.loader import get_template
from django.test import TestCase, RequestFactory
from django.core.signing import Signer

from unittest import expectedFailure

from core.utils import (extract_answers_from_request,
                        hash_for_script,
                        add_js_hash_to_request,
                        sign_url,
                        append_query_args_to_url)


class FakeRequest(object):
    # Quick way to simulate a request object with a POST attribute
    def __init__(self, params):
        self.POST = params


class JavascriptHashTest(TestCase):
    script = "alert('hello javascript');"
    expected_sha = "'sha256-Ft3A+V6Yme/8r0/K/uC38Zj0VJ98VnbTD3MLupPTNuc='"

    def test_hash_generation(self):
        hash = hash_for_script(self.script)
        self.assertEqual(hash, self.expected_sha)

    def test_adding_sha_to_request(self):
        factory = RequestFactory()
        request = factory.get('/')
        add_js_hash_to_request(request, self.script)
        self.assertIn(self.expected_sha, request.script_hashes)


class CSPTemplateTagsTest(TestCase):
    factory = RequestFactory()
    expected_sha = "'sha256-SypW8zp5ZrylvHKnRaTv4V9wLQxdi9hBpjLLWAzN4Xw='"

    def render_and_check_sha(self, template):
        request = self.factory.get('/')
        template.render({}, request=request)
        self.assertIn(self.expected_sha, request.script_hashes)

    # this test is non-viable until we factor out the need for SheerLikeContext
    @expectedFailure
    def test_jinja2_tag(self):
        template = get_template('test-fixture/csp-jinja2.html',
                                using='wagtail-env')

        self.render_and_check_sha(template)

    def test_django_tag(self):
        template = get_template('test-fixture/csp-django.html')

        self.render_and_check_sha(template)


class URLBuildingTest(TestCase):
    def test_append_query_args(self):
        query_args = {'foo': 'bar'}
        base_url = 'http://google.com/'
        result = append_query_args_to_url(base_url, query_args)
        self.assertEqual(result, 'http://google.com/?foo=bar')


class URLSigningTest(TestCase):
    def test_signing_url(self):
        key = 'testkey'
        url, signature = sign_url('http://google.com', secret=key)
        # this is the default format for signing results in Django
        recombined = "{0}:{1}".format(url, signature)

        signer = Signer(key)
        unsigned_url = signer.unsign(recombined)

        self.assertEqual(url, unsigned_url)


class ExtractAnswersTest(TestCase):

    def test_no_answers_to_extract(self):
        request = FakeRequest({'unrelated_key': 'unrelated_value'})
        result = extract_answers_from_request(request)
        assert result == []

    def test_multiple_answers_to_extract(self):
        request = FakeRequest({'unrelated_key': 'unrelated_value',
                               'questionid_first': 'some_answer',
                               'questionid_another': 'another_answer'})
        result = extract_answers_from_request(request)
        assert sorted(result) == [('another', 'another_answer'),
                                  ('first', 'some_answer')]
