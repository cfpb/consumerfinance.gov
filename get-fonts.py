import argparse
import os
import os.path
import sys

import requests

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


message = """
By continuing, you acknowledge that the fonts being downloaded are
NOT subject to the terms described in 'LICENSE', and assert that
you have permission to use these files.
"""


def download_fonts():
    font_dir = "static.in/cfgov-fonts/"

    staticfiles_manifest = requests.get(
        "https://www.consumerfinance.gov/static/staticfiles.json"
    ).json()

    paths = staticfiles_manifest["paths"]
    fonts = ((k, paths[k]) for k in paths.keys() if k.startswith("fonts/"))

    for name, hashed_name in fonts:
        destination_path = os.path.join(font_dir, name)
        url = urlparse.urljoin(
            "https://www.consumerfinance.gov/static/", hashed_name
        )
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # we download using the "hashed" name to take advantage of the
        # more agressive CDN cache for those URL's
        with open(destination_path, "wb") as destination:
            response = requests.get(url)
            destination.write(response.content)
            print("wrote %s to %s" % (url, destination_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--agree", choices=("yes", "no"), default="no", help=message)

    args = parser.parse_args()
    if args.agree and args.agree == "yes":
        download_fonts()
    else:
        parser.print_help()
        sys.exit(1)
