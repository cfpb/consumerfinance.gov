import datetime
import os
import sys
import tempfile

from django.test import TestCase

from retirement_api.models import (
    AgeChoice,
    Calibration,
    Page,
    Question,
    Step,
    Tooltip,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class ViewModels(TestCase):

    testagechoice = AgeChoice(age=62, aside="Aside.")
    testquestion = Question(
        title="Test Question", slug="", question="Test question."
    )
    teststep = Step(title="Test Step")
    testpage = Page(title="Page title", intro="Intro")
    testtip = Tooltip(title="Test Tooltip")
    testcalibration = Calibration(created=datetime.datetime.now())

    def test_calibration(self):
        self.assertTrue("calibration" in self.testcalibration.__unicode__())

    def test_get_subhed(self):
        tc = self.testagechoice
        self.assertTrue("You've chosen age 62" in tc.get_subhed())

    def test_question_slug(self):
        self.testquestion.save()
        self.assertTrue(self.testquestion.slug != "")

    def test_question_translist(self):
        tlist = self.testquestion.translist()
        self.assertTrue(type(tlist) == list)
        for term in [
            "question",
            "answer_yes_a",
            "answer_no_b",
            "answer_unsure_a_subhed",
        ]:
            self.assertTrue(term in tlist)

    def test_question_dump(self):
        with tempfile.NamedTemporaryFile() as f:
            self.testquestion.dump_translation_text(
                output=True, outfile=f.name
            )

            f.seek(0)
            translation_po_file_content = f.read()

            self.assertEqual(
                translation_po_file_content,
                (
                    b"""\
msgid ""
msgstr ""
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Project-Id-Version: retirement\\n"
"Language: es\\n"

#: templates/claiming.html
msgid "Test question."
msgstr ""

"""
                ),
            )

    def test_question_dump_no_output(self):
        dump = self.testquestion.dump_translation_text()
        self.assertEqual("Test question.", dump[0])

    def test_agechoice_translist(self):
        tlist = self.testagechoice.translist()
        self.assertTrue(type(tlist) == list)

    def test_step_translist(self):
        tlist = self.teststep.translist()
        self.assertTrue(type(tlist) == list)

    def test_page_translist(self):
        tlist = self.testpage.translist()
        self.assertTrue(type(tlist) == list)

    def test_tooltip_translist(self):
        tlist = self.testtip.translist()
        self.assertTrue(type(tlist) == list)
