from django.test import SimpleTestCase

from tccp.widgets import OrderingSelect, RadioSelect


class RadioSelectTests(SimpleTestCase):
    def test_init_without_attrs_sets_class(self):
        self.assertEqual(RadioSelect().attrs, {"class": "a-radio"})

    def test_init_with_attrs_sets_class(self):
        self.assertEqual(
            RadioSelect(attrs={"foo": "bar"}).attrs,
            {"class": "a-radio", "foo": "bar"},
        )

    def test_init_with_attrs_keeps_class_if_set(self):
        self.assertEqual(
            RadioSelect(attrs={"class": "a-something-else"}).attrs,
            {"class": "a-something-else"},
        )


class OrderingSelectTests(SimpleTestCase):
    def test_init_without_attrs_sets_class(self):
        self.assertEqual(OrderingSelect().attrs, {"form": "tccp-filters"})
