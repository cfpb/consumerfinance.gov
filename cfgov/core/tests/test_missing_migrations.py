from six.moves import cStringIO as StringIO

from django.test import TestCase

from core.scripts.missing_migrations import migrations_are_missing


class MissingMigrationsTestCase(TestCase):
    def test_check_for_missing_migrations(self):
        if migrations_are_missing(out=StringIO()):
            self.fail('missing migrations, run manage.py makemigrations')
