import os
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from PIL import Image


def create_image(size=(100, 100), image_mode="RGB", image_format="PNG"):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return data


class TestAddImages(TestCase):
    def setUp(self):
        self.filename = os.path.join(
            settings.PROJECT_ROOT, "legacy/static/images/cfpblogo.png"
        )
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.user = User.objects.get(pk=1)

    def test_add_image(self):
        filename_only = os.path.split(self.filename)[-1]
        logo = create_image()
        image_file = SimpleUploadedFile(filename_only, logo.getvalue())
        post_data = {
            "title": filename_only,
            "file": image_file,
        }
        response = self.client.post("/", post_data, follow=True)
        self.assertEqual(response.status_code, 400)
