from django.db import models
from unittest import TestCase

from cfgov.test import HtmlMixin
from v1.atomic_elements.organisms import ModelBlock, ModelTable


class TestModel(models.Model):
    name = models.CharField(max_length=16)
    age = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)


class TestModelMixin(object):
    @classmethod
    def setUpClass(cls):
        names = ['chico', 'harpo', 'groucho']
        ages = [50, 60, 60]

        TestModel.objects.bulk_create([
            TestModel(name=name, age=age) for name, age in zip(names, ages)
        ])


class ModelBlockTestCase(TestModelMixin, TestCase):
    def test_get_queryset_default(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['chico', 'harpo', 'groucho']
        )

    def test_get_queryset_filtering(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'

            def filter_queryset(self, qs, value):
                return qs.filter(name__startswith='h')

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['harpo']
        )

    def test_get_queryset_single_ordering(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'
            ordering = '-name'

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['harpo', 'groucho', 'chico']
        )

    def test_get_queryset_ordering_method(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'

            def get_ordering(self, value):
                return '-name'

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['harpo', 'groucho', 'chico']
        )

    def test_get_queryset_multiple_orderings(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'
            ordering = ('-age', '-name')

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['harpo', 'groucho', 'chico']
        )

    def test_get_queryset_limit(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'
            limit = 2

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['chico', 'harpo']
        )

    def test_get_queryset_limit_method(self):
        class TestModelBlock(ModelBlock):
            model = 'v1.TestModel'

            def get_limit(self, value):
                return 2

        block = TestModelBlock()
        self.assertSequenceEqual(
            [model.name for model in block.get_queryset(None)],
            ['chico', 'harpo']
        )


class ModelTableTestCase(TestModelMixin, HtmlMixin, TestCase):
    def test_default_formatter(self):
        self.assertEqual(
            ModelTable().format_field_value(None, 'foo', 1234),
            '1234'
        )

    def test_custom_formatter(self):
        class TestModelTable(ModelTable):
            def make_foo_value(self, instance, value):
                return str(2 * value)

        self.assertEqual(
            TestModelTable().format_field_value(None, 'foo', 1234),
            '2468'
        )

    def test_headers(self):
        class TestModelTable(ModelTable):
            model = 'v1.TestModel'
            fields = ('name', 'age')
            field_headers = ('First Name', 'Age')

        table = TestModelTable()
        html = table.render(table.to_python({}))

        self.assertHtmlRegexpMatches(html, (
            '<thead>'
            '<tr>'
            '<th>First Name</th>'
            '<th>Age</th>'
            '</tr>'
            '</thead>'
        ))
