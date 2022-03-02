from unittest import mock

from django.test import TestCase

from scripts import _atomic_helpers as atomic
from v1.models import BlogPage, LearnPage, NewsroomPage, SublandingPage
from v1.tests.wagtail_pages.helpers import publish_changes, publish_page
from v1.util.migrations import set_streamfield_data


class TestEmailSignup(TestCase):
    def check_page_content(self, page_cls, field):
        page = page_cls(slug="slug", title="title")
        publish_page(child=page)

        set_streamfield_data(page, field, [atomic.email_signup])
        publish_changes(child=page)

        response = self.client.get("/slug/")
        self.assertContains(response, "Email Sign Up")

    def test_sublanding_page_sidebar(self):
        self.check_page_content(SublandingPage, "sidefoot")

    def test_blog_page_content(self):
        self.check_page_content(BlogPage, "content")

    def test_learn_page_content(self):
        self.check_page_content(LearnPage, "content")

    @mock.patch("v1.models.caching.AkamaiBackend.post_tags")
    def test_newsroom_page_content(self, mock_post_tags):
        self.check_page_content(NewsroomPage, "content")
