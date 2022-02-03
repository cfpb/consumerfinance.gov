import os
import shutil
import tempfile
from unittest import skipUnless

from django.core.management import call_command
from django.core.management.utils import find_command
from django.test import SimpleTestCase


# https://github.com/django/django/blob/1.11.18/tests/i18n/test_extraction.py
has_xgettext = find_command('xgettext')


@skipUnless(has_xgettext, 'xgettext is mandatory for extraction tests')
class TestCustomMakeMessages(SimpleTestCase):
    DATA_DIR = 'test_makemessages_data'

    LOCALE = 'de'

    PO_FILE = 'locale/%s/LC_MESSAGES/django.po' % LOCALE

    def setUp(self):
        # https://github.com/django/django/blob/1.11.18/tests/i18n/utils.py#L33
        self._cwd = os.getcwd()

        # Create a temporary test directory to extract messages from.
        self.temp_dir = tempfile.mkdtemp()

        # Copy test data to temporary test directory.
        test_dir = os.path.join(self.temp_dir, self.DATA_DIR)
        shutil.copytree(
            os.path.join(os.path.dirname(__file__), self.DATA_DIR),
            test_dir,
            ignore=shutil.ignore_patterns('*.pyc', '__pycache__')
        )

        # Create a destination locale directory in the temp directory. We don't
        # include this in the source data being copied because we don't want it
        # to be in the source tree when makemigrations is run normally.
        os.mkdir(os.path.join(test_dir, 'locale'))

        # Remove the temporary test directory on cleanup.
        self.addCleanup(self._rmrf, self.temp_dir)

        # Change back to the previous working directory on cleanup.
        self.addCleanup(os.chdir, self._cwd)

        # Change to the test directory so that running makemessages both reads
        # the files located there and writes its output there.
        os.chdir(test_dir)

    def _rmrf(self, dname):
        # Only remove this location if we're really deleting the right thing.
        # https://github.com/django/django/blob/1.11.18/tests/i18n/utils.py
        if (
            os.path.commonprefix([self.temp_dir, os.path.abspath(dname)]) !=
            self.temp_dir
        ):
            return

        shutil.rmtree(dname)

    def test_extraction_works_as_expected_including_jinja2_block(self):
        call_command('makemessages', locale=[self.LOCALE], verbosity=0)

        with open(self.PO_FILE, 'r') as f:
            contents = f.read()

        expected = '''
#: __init__.py:4
msgid "Test string from Python file."
msgstr ""

#: jinja2/test.html:1
msgid ""
"\\n"
"Test string from Jinja template.\\n"
"This is in a multi-line block.\\n"
msgstr ""

#: templates/test.html:2
msgid "Test string from Django template."
msgstr ""
'''

        self.assertIn(expected, contents)
