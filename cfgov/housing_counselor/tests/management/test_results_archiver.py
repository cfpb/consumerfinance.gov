import json
import os
import shutil
from tempfile import mkdtemp
from unittest import TestCase
from zipfile import ZipFile

from housing_counselor.results_archiver import json_file_name, save_list


class TestHousingCounselorResultsArchiver(TestCase):
    def setUp(self):
        self.temp_directory = mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_directory)

    def test_save_list_creates_zip_file(self):
        content = [
            {"fake": 1, "housing": "counselor", "json": 2},
            {"fake": 3, "housing": "data", "json": 4},
        ]
        zip_path = os.path.join(self.temp_directory, "archive.zip")

        save_list(content, zip_path)
        with ZipFile(zip_path) as zip_file:
            zip_content = json.loads(zip_file.read(json_file_name))
            self.assertEqual(zip_content, content)
