from django.apps import apps
from django.test import TestCase

from v1.models.base import CFGOVPage


class PageSettingsOrderTestCaseMeta(type):
    def __new__(cls, name, parent, dct):
        for app in apps.get_app_configs():
            for model in app.get_models():
                if issubclass(model, CFGOVPage):
                    cls.add_test(dct, model)

        return super().__new__(cls, name, parent, dct)

    @classmethod
    def add_test(cls, dct, page_cls):
        def fn(self):
            self.check_correct_page_settings_order(page_cls)

        cls_name = page_cls.__name__.lower()
        test_name = "test_correct_page_settings_order_{}".format(cls_name)
        fn.__name__ = test_name
        dct[test_name] = fn


class PageSettingsOrderTestCase(TestCase):
    __metaclass__ = PageSettingsOrderTestCaseMeta

    expected_panel_order = (
        "settings",
        "categories",
        "tags",
        "page preview fields",
        "authors",
        "relevant dates",
        "scheduled publishing",
        "language",
    )

    def check_correct_page_settings_order(self, page_cls):
        settings_panels = getattr(page_cls, "settings_panels", [])
        panel_names = [self.get_panel_name(p).lower() for p in settings_panels]
        expected_order = [
            p for p in self.expected_panel_order if p in panel_names
        ]

        self.assertSequenceEqual(panel_names, expected_order)

    def get_panel_name(self, panel):
        name_keys = ("heading", "field_name", "relation_name")
        for name_key in name_keys:
            name = getattr(panel, name_key, None)

            if name:
                return name
