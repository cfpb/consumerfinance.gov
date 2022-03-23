import os

import requests
import requests.exceptions


class SyncStorageCommandMixin:
    def add_arguments(self, parser):
        parser.add_argument(
            "base_url", help="ex: https://files.consumerfinance.gov/f/"
        )
        parser.add_argument("dest_dir", help="ex: ./cfgov/f/")

    def handle(self, *args, **options):
        self.base_url = options["base_url"]
        self.dest_dir = options["dest_dir"]

        for subdir in self.get_storage_directories():
            directory = os.path.join(self.dest_dir, subdir)
            if not os.path.exists(directory):
                os.makedirs(directory)

        queryset = self.get_queryset()
        count = queryset.count()

        for i, instance in enumerate(queryset):
            log_prefix = "%d/%d (%d) " % (i + 1, count, instance.pk)
            self.handle_instance(instance, log_prefix)

    def get_storage_subdirectories():
        raise NotImplementedError

    def get_queryset():
        raise NotImplementedError

    def handle_instance(self, instance, log_prefix):
        self.stdout.write(log_prefix, ending="")
        self.save(instance.file.name)

    def save(self, path):
        url = self.base_url + path
        filename = self.dest_dir + path

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
