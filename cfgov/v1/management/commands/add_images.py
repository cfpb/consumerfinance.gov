import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse

from wagtail.images import get_image_model

from v1.management.commands._utils import WagtailClient


class Command(WagtailClient, BaseCommand):
    help = "Adds one or more Wagtail images"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", help="image filename")

    def handle(self, *args, **options):
        if not self.login():
            raise CommandError("login failure")

        filenames = options["filename"]

        failures = []
        for filename in filenames:
            try:
                self.add_image(filename)
            except Exception as e:
                self.stderr.write("failed to add image {}".format(filename))
                self.stderr.write(str(e))
                failures.append(filename)

        if failures:
            raise CommandError("failed to add images: {}".format(filenames))

    def add_image(self, filename):
        filename_only = os.path.split(filename)[-1]

        with open(filename, "rb") as f:
            image_file = SimpleUploadedFile(filename_only, f.read())

        response = self.client.post(
            reverse("wagtailimages:add"),
            {
                "title": filename_only,
                "file": image_file,
            },
        )

        if 302 != response.status_code:
            raise RuntimeError("something went wrong: {}".format(response))

        image_model = get_image_model()
        image = image_model.objects.filter(title=filename_only).latest("pk")

        self.stdout.write("added image {}: {}".format(image.pk, image))
