import datetime

from django.test import RequestFactory, TestCase

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site

import pytz

from scripts import fix_links_in_tableblocks
from v1.models import DocumentDetailPage, EventPage, LearnPage
from v1.tests.wagtail_pages.helpers import save_new_page


class TestFixLinksInTableblocks(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.doc_table_block = {
            "type": "table_block",
            "value": {
                "data": [
                    [
                        '<a href="/documents/6881/cfpb.pdf" id="6881" '
                        + 'linktype="document">Read/download</a>'
                    ]
                ]
            },
        }
        self.file_table_block = {
            "type": "table_block",
            "value": {
                "data": [
                    [
                        '<a href="https://files.consumerfinance.gov'
                        + '/f/cfpb.pdf">Read/download</a>'
                    ]
                ]
            },
        }
        self.page_table_block = {
            "type": "table_block",
            "value": {
                "data": [
                    [
                        '<a href="/rules-policy/final-rules/escrow/" '
                        + 'id="1123" linktype="page">Escrows</a>'
                    ]
                ]
            },
        }
        self.root = Site.objects.get(is_default_site=True).root_page
        self.doc_page = DocumentDetailPage(
            title="Document", live=True, slug="document"
        )
        self.event_page = EventPage(
            title="Event",
            live=True,
            slug="event",
            start_dt=datetime.datetime.now(pytz.UTC),
            venue_city="Detroit",
            venue_state="MI",
        )
        self.learn_page = LearnPage(title="Learn", live=True, slug="learn")
        self.doc_page.specific.content = StreamValue(
            self.doc_page.specific.content.stream_block,
            [self.doc_table_block],
            True,
        )
        self.event_page.specific.content = StreamValue(
            self.event_page.persistent_body.stream_block,
            [self.page_table_block],
            True,
        )
        self.learn_page.specific.content = StreamValue(
            self.learn_page.specific.content.stream_block,
            [{"type": "full_width_text", "value": [self.file_table_block]}],
            True,
        )
        save_new_page(self.doc_page, root=self.root)
        save_new_page(self.event_page, root=self.root)
        save_new_page(self.learn_page, root=self.root)

    def test_fix_links_in_tableblocks(self):
        fix_links_in_tableblocks.run()

        doc_request = self.factory.get("/document/")
        event_request = self.factory.get("/event/")
        learn_request = self.factory.get("/learn/")

        response = self.doc_page.serve(doc_request)
        self.assertContains(response, "href=")

        response = self.event_page.serve(event_request)
        self.assertContains(response, "href=")

        response = self.learn_page.serve(learn_request)
        self.assertContains(response, "href=")
