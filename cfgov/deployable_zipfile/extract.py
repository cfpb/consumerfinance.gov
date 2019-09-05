#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
from zipfile import ZipFile


def extract_zipfile(zipfile_filename, extract_location):
    zipfile = ZipFile(zipfile_filename)

    # Extract all files except for this extraction script.
    zipfile.extractall(
        extract_location,
        [f for f in zipfile.namelist() if f != __name__]
    )

    # Create a new virtual environment with pip and setuptools from the
    # bootstrap wheels included in the zipfile.
    virtualenv_dir = os.path.join(extract_location, 'venv')
    bootstrap_wheel_dir = os.path.join(extract_location, 'bootstrap_wheels')

    subprocess.check_call([
        sys.executable,
        '-m',
        'virtualenv',
        '--never-download',
        '--no-wheel',
        '--extra-search-dir=%s' % bootstrap_wheel_dir,
        virtualenv_dir,
    ])

    # Run the setup script inside that new virtual environment.
    virtualenv_python = os.path.join(virtualenv_dir, 'bin', 'python')
    setup_script = os.path.join(extract_location, 'setup.py')

    subprocess.check_call([virtualenv_python, setup_script])

    # Cleanup by removing the bootstrap wheels directory and setup script.
    shutil.rmtree(bootstrap_wheel_dir)
    os.unlink(setup_script)


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Extract a deployable Django project zipfile'
    )

    parser.add_argument('zipfile_filename', nargs='?')
    parser.add_argument('-d', '--destination', dest='extract_location',
                        required=True)

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
