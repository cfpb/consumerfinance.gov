import random
from unittest.mock import patch

from django.core.paginator import Page
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from agreements import models


def agreement_factory(**kwargs):
    """
    Create an agreement with some defaults.
    """
    if "issuer" not in kwargs:
        kwargs["issuer"] = models.Issuer(name="")
        kwargs["issuer"].save()

    args = {
        "file_name": "",
        "size": 0,
        "uri": "https://example.com",
        "description": "",
    }

    for key in kwargs:
        args[key] = kwargs[key]
    agreement = models.Agreement(**args)

    agreement.save()

    return agreement


class Views(TestCase):
    @patch("agreements.views.render", return_value=HttpResponse())
    def test_index_empty(self, render):
        """
        Test index without any agreements.
        """
        self.client.get(reverse("agreements_home"))
        context = render.call_args[0][2]

        self.assertTrue("pagetitle" in context)
        self.assertTrue(len(context["pagetitle"]) > 5)
        self.assertTrue("agreement_count" in context)
        self.assertEqual(0, context["agreement_count"])

    def test_index_renders(self):
        response = self.client.get(reverse("agreements_home"))
        str(response.content.decode("utf-8"))

    @patch("agreements.views.render", return_value=HttpResponse())
    def test_index_with_agreements(self, render):
        """
        Test index with some agreements.
        """
        count = random.randint(3, 10)

        for _ in range(count):
            agreement_factory()

        self.client.get(reverse("agreements_home"))
        context = render.call_args[0][2]

        self.assertTrue("agreement_count" in context)
        self.assertEqual(count, context["agreement_count"])

    def test_issuer_search_404(self):
        """
        Verify that retrieving a non-existent issuer results in a 404.
        """
        response = self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": "99999"})
        )
        self.assertEqual(response.status_code, 404)

    @patch("agreements.views.render", return_value=HttpResponse())
    def test_issuer_correct_keys(self, render):
        """
        Verify that the fields in the context are those expected by the
        template.
        """
        issuer = models.Issuer(name="name", slug="slug")
        issuer.save()

        self.client.get(
            reverse("issuer_search", kwargs={"issuer_slug": issuer.slug})
        )
        context = render.call_args[0][2]

        self.assertTrue("page" in context)
        self.assertTrue(isinstance(context["page"], Page))
        self.assertTrue("issuer" in context)
        self.assertEqual(issuer, context["issuer"])

    @patch("agreements.views.render", return_value=HttpResponse())
    def test_issuer_paging_backend(self, render):
        """
        Verify that the pager is working.
        """
        issuer = models.Issuer(name="name", slug="slug")
        issuer.save()
        for _ in range(45):
            agreement_factory(issuer=issuer)

        path = reverse("issuer_search", kwargs={"issuer_slug": issuer.slug})
        self.client.get(path)
        context = render.call_args[0][2]

        self.assertTrue("page" in context)
        self.assertEqual(40, len(context["page"].object_list))

        self.client.get(path + "?page=2")
        context = render.call_args[0][2]

        self.assertTrue("page" in context)
        self.assertEqual(5, len(context["page"].object_list))

    def test_issuer_paging_frontend(self):
        """
        Verify that the pager has links in HTML.
        """
        issuer = models.Issuer(name="name", slug="slug")
        issuer.save()
        for _ in range(45):
            agreement_factory(issuer=issuer)

        path = reverse("issuer_search", kwargs={"issuer_slug": issuer.slug})
        resp = self.client.get(path)
        self.assertContains(resp, "page=2")
        self.assertNotContains(resp, "page=1")
        self.assertFalse(b"page=1" in resp.content)

        resp = self.client.get(path + "?page=2")
        self.assertContains(resp, 'href="?page=1')
        self.assertNotContains(resp, 'href="?page=2')
        self.assertNotContains(resp, 'href="?page=3')

    @patch("agreements.views.render", return_value=HttpResponse())
    def test_issuer_paging_too_high(self, render):
        """
        Verify that the pager is working when page number is too high.
        """
        issuer = models.Issuer(name="name", slug="slug")
        issuer.save()
        for _ in range(45):
            agreement_factory(issuer=issuer)

        path = reverse("issuer_search", kwargs={"issuer_slug": issuer.slug})
        self.client.get(path + "?page=2")
        object_ids2 = list(
            map(lambda o: o.id, render.call_args[0][2]["page"].object_list)
        )

        self.client.get(path + "?page=5555")
        object_ids5555 = list(
            map(lambda o: o.id, render.call_args[0][2]["page"].object_list)
        )

        self.assertEqual(5, len(object_ids2))
        self.assertEqual(5, len(object_ids5555))
        self.assertEqual(object_ids2, object_ids5555)

    @patch("agreements.views.render", return_value=HttpResponse())
    def test_issuer_paging_non_int(self, render):
        """
        Verify that the pager is working when page number is not an int.
        """
        issuer = models.Issuer(name="")
        issuer.save()
        for _ in range(45):
            agreement_factory(issuer=issuer)

        path = reverse("issuer_search", kwargs={"issuer_slug": issuer.slug})
        self.client.get(path + "?page=1")
        object_ids1 = list(
            map(lambda o: o.id, render.call_args[0][2]["page"].object_list)
        )

        self.client.get(path + "?page=abcd")
        object_idsabcd = list(
            map(lambda o: o.id, render.call_args[0][2]["page"].object_list)
        )
        self.assertEqual(40, len(object_ids1))
        self.assertEqual(40, len(object_idsabcd))
        self.assertEqual(object_ids1, object_idsabcd)
