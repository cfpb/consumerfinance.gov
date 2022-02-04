from django.contrib.auth.models import User
from django.test import TestCase

from v1.atomic_elements.organisms import ModelBlock


class UserModelMixin(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
