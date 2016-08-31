from django.contrib.auth.models import User
from django.test import TestCase

from cfgov.test import HtmlMixin
from v1.atomic_elements.organisms import ModelBlock, ModelTable


class UserModelMixin(object):
    @classmethod
    def setUpClass(cls):
        super(UserModelMixin, cls).setUpClass()
        usernames = ['chico', 'harpo', 'groucho']
        first_names = ['leonard', 'arthur', 'julius']

        User.objects.bulk_create([
            User(username=username, first_name=first_name)
            for (username, first_name) in zip(usernames, first_names)
        ])


class ModelBlockTestCase(UserModelMixin, TestCase):
    def test_get_queryset_default(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['admin', 'chico', 'harpo', 'groucho']
        )

    def test_get_queryset_filtering(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'

            def filter_queryset(self, qs, value):
                return qs.filter(username__startswith='h')

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['harpo']
        )

    def test_get_queryset_single_ordering(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'
            ordering = '-username'

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['harpo', 'groucho', 'chico', 'admin']
        )

    def test_get_queryset_ordering_method(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'

            def get_ordering(self, value):
                return '-username'

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['harpo', 'groucho', 'chico', 'admin']
        )

    def test_get_queryset_multiple_orderings(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'
            ordering = ('-first_name', '-username')

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['chico', 'groucho', 'harpo', 'admin']
        )

    def test_get_queryset_limit(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'
            limit = 2

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['admin', 'chico']
        )

    def test_get_queryset_limit_method(self):
        class UserBlock(ModelBlock):
            model = 'auth.User'

            def get_limit(self, value):
                return 2

        block = UserBlock()
        self.assertSequenceEqual(
            [model.username for model in block.get_queryset(None)],
            ['admin', 'chico']
        )


class ModelTableTestCase(UserModelMixin, HtmlMixin, TestCase):
    def test_default_formatter(self):
        self.assertEqual(
            ModelTable().format_field_value(None, 'foo', 1234),
            '1234'
        )

    def test_custom_formatter(self):
        class UserTable(ModelTable):
            def make_foo_value(self, instance, value):
                return str(2 * value)

        self.assertEqual(
            UserTable().format_field_value(None, 'foo', 1234),
            '2468'
        )

    def get_table_html(self, **kwargs):
        class UserTable(ModelTable):
            model = 'auth.User'
            fields = ('username', 'first_name')
            field_headers = ('Username', 'First Name')

        table = UserTable()
        return table.render(table.to_python(kwargs))

    def test_no_row_headers(self):
        html = self.get_table_html(first_row_is_table_header=False)
        self.assertHtmlRegexpMatches(html, (
            '<tbody>'
            '<tr>'
            '<td data-label="Username">Username</td>'
            '<td data-label="First Name">First Name</td>'
            '</tr>'
        ))

    def test_row_headers(self):
        html = self.get_table_html(first_row_is_table_header=True)
        self.assertHtmlRegexpMatches(html, (
            '<thead>'
            '<tr>'
            '<th>Username</th>'
            '<th>First Name</th>'
            '</tr>'
            '</thead>'
        ))

    def test_no_col_headers(self):
        html = self.get_table_html(first_col_is_header=False)
        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<td data-label="Username">chico</td>'
            '<td data-label="First Name">leonard</td>'
            '</tr>'
        ))

    def test_col_headers(self):
        html = self.get_table_html(first_col_is_header=True)
        self.assertHtmlRegexpMatches(html, (
            '<tr>'
            '<th data-label="Username">chico</th>'
            '<td data-label="First Name">leonard</td>'
            '</tr>'
        ))

    def test_no_full_width(self):
        html = self.get_table_html(is_full_width=False)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table">'
        ))

    def test_full_width(self):
        html = self.get_table_html(is_full_width=True)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table u-w100pct">'
        ))

    def test_not_striped(self):
        html = self.get_table_html(is_striped=False)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table">'
        ))

    def test_striped(self):
        html = self.get_table_html(is_striped=True)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table table__striped">'
        ))

    def test_not_stacked(self):
        html = self.get_table_html(is_stacked=False)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table">'
        ))

    def test_stacked(self):
        html = self.get_table_html(is_stacked=True)
        self.assertHtmlRegexpMatches(html, (
            '<table class="o-table table__stack-on-small">'
        ))
