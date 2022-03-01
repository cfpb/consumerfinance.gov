#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
from glob import glob
from zipfile import ZipFile


def locate_virtualenv_site_packages(virtualenv_python):
    # On some systems, depending on how sys.stdout is configured, a default
    # encoding may not be configured. Use utf-8 as a fallback.
    stdout_encoding = getattr(sys.stdout, "encoding", None) or "utf-8"

    return (
        subprocess.check_output(
            [
                virtualenv_python,
                "-c",
                "import sys; print(sys.path[-1])",
            ]
        )
        .decode(stdout_encoding)
        .strip()
    )


def extract_zipfile(zipfile_filename, extract_location):
    # Extract all files to the extract location.
    ZipFile(zipfile_filename).extractall(extract_location)

    # Create a new virtual environment with pip and setuptools from the
    # bootstrap wheels included in the zipfile.
    virtualenv_dir = os.path.join(extract_location, "venv")
    bootstrap_wheels = os.path.join(extract_location, "bootstrap_wheels")

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "virtualenv",
            "--never-download",
            "--no-wheel",
            "--extra-search-dir=%s" % bootstrap_wheels,
            virtualenv_dir,
        ]
    )

    # Store the path to the new virtual environment's site-packages. At this
    # point before any other packages have been installed, this will always be
    # the last entry in the Python path.
    virtualenv_python = os.path.join(virtualenv_dir, "bin", "python")

    site_packages = locate_virtualenv_site_packages(virtualenv_python)

    # Install project dependencies from the wheels directory, but only those
    # that are compatible with the version of Python being used.
    wheel_install_script = os.path.join(extract_location, "install_wheels.py")
    wheels = os.path.join(extract_location, "wheels")

    subprocess.check_call(
        [
            virtualenv_python,
            wheel_install_script,
            wheels,
        ]
    )

    # Move .pth files into the virtual environment site-packages so that they
    # they get processed on Python startup.
    for pth_file in glob("%s/*.pth" % extract_location):
        shutil.move(pth_file, site_packages)

    # Also move the loadenv.py script to support automatic loading of
    # environment variables.
    shutil.move(os.path.join(extract_location, "loadenv.py"), site_packages)

    # Cleanup by removing the wheel directories and install scripts.
    shutil.rmtree(bootstrap_wheels)
    shutil.rmtree(wheels)
    os.unlink(wheel_install_script)
    os.unlink(os.path.join(extract_location, "__main__.py"))


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Extract a deployable Django project zipfile"
    )

    parser.add_argument("zipfile_filename", nargs="?")
    parser.add_argument("-d", "--destination", dest="extract_location", required=True)

    args = parser.parse_args()

    if not args.zipfile_filename:
        # If a zipfile filename hasn't been provided, this script might have
        # been invoked as part of a self-extracting zipfile's __main__.py.
        try:
            args.zipfile_filename = __loader__.archive  # noqa F821
        except AttributeError:
            parser.print_help()
            sys.exit(1)

    extract_zipfile(**vars(args))
