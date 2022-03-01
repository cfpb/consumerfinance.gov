import os

from django.core.management.base import BaseCommand

from wagtail.images import get_image_model

import requests
import requests.exceptions


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "base_url", help="ex: https://files.consumerfinance.gov/f/"
        )
        parser.add_argument("dest_dir", help="ex: ./cfgov/f/")

    def handle(self, *args, **options):
        base_url = options["base_url"]
        dest_dir = options["dest_dir"]

        for subdir in ("images", "original_images"):
            directory = os.path.join(dest_dir, subdir)
            if not os.path.exists(directory):
                os.makedirs(directory)

        images = get_image_model().objects.all()
        image_count = images.count()

        for i, image in enumerate(images):
            image_prefix = "%d/%d (%d) " % (i + 1, image_count, image.pk)
            self.stdout.write(image_prefix, ending="")
            self.save(base_url, dest_dir, image.file.name)

            renditions = image.renditions.all()
            rendition_count = renditions.count()

            for j, rendition in enumerate(renditions):
                rendition_prefix = "%d/%d (%d) " % (
                    j + 1,
                    rendition_count,
                    rendition.pk,
                )
                self.stdout.write(image_prefix + rendition_prefix, ending="")
                self.save(base_url, dest_dir, rendition.file.name)

    def save(self, base_url, dest_dir, path):
        url = base_url + path
        filename = dest_dir + path

        self.stdout.write("Saving %s to %s\n" % (url, filename))

        response = requests.get(url, stream=True)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.stderr.write(str(e))
        else:
            with open(filename, "wb") as f:
                for block in response.iter_content(1024):
                    f.write(block)
