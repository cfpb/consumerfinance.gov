from unittest.mock import patch

from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from agreements.models import Agreement, Issuer
from agreements.views import archive, index, issuer_search


class TestIssuerSearch(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_no_issuers_raises_404(self):
        with self.assertRaises(Http404):
            issuer_search(self.request, "none")

    def test_missing_issuer_raises_404(self):
        Issuer.objects.create(name="name", slug="slug")
        with self.assertRaises(Http404):
            issuer_search(self.request, "missing")

    def test_issuer_no_agreements(self):
        Issuer.objects.create(name="A & B Bank", slug="a-b-bank")
        response = self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": "a-b-bank"})
        )
        self.assertContains(response, "A &amp; B Bank")

    def test_issuer_has_agreements(self):
        issuer = Issuer.objects.create(name="A & B Bank", slug="a-b-bank")
        for i in range(2):
            filename = f"agreement{i + 1}.pdf"
            Agreement.objects.create(
                issuer=issuer, description=filename, file_name=filename, size=0
            )

        response = self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": "a-b-bank"})
        )
        self.assertContains(response, "agreement1.pdf")
        self.assertContains(response, "agreement2.pdf")

    def test_multiple_issuers_with_same_slug_no_agreements_uses_latest(self):
        Issuer.objects.create(name="A & B Bank", slug="a-b-bank")
        Issuer.objects.create(name="A - B Bank", slug="a-b-bank")
        response = self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": "a-b-bank"})
        )
        self.assertContains(response, "A - B Bank")

    def test_multiple_issuers_with_same_slug_uses_latest_agreement(self):
        issuer = Issuer.objects.create(name="A & B Bank", slug="a-b-bank")
        Agreement.objects.create(
            issuer=issuer,
            description="description",
            file_name="filename",
            size=0,
        )

        Issuer.objects.create(name="A - B Bank", slug="a-b-bank")
        response = self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": "a-b-bank"})
        )
        self.assertContains(response, "A &amp; B Bank")


class TestIndexRender(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    @patch("agreements.views.render")
    def test_index(self, render):
        index(self.request)

        render.assert_called_with(
            self.request,
            "agreements/index.html",
        )


class TestArchiveRender(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("agreements_archive"))

    @patch("agreements.views.Metadata")
    @patch("agreements.views.render")
    def test_archive(self, render, Metadata):
        archive(self.request)

        render.assert_called_with(
            self.request,
            "agreements/archive.html",
            {
                "agreements": Metadata().get_sorted_agreements(),
                "flexibilities": Metadata().flexibilities,
                "notes": Metadata().notes,
            },
        )
