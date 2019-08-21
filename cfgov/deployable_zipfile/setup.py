import os
import shutil
import subprocess
import sys
from glob import glob

from pip._internal.exceptions import InstallationError
from pip._internal.req.constructors import install_req_from_line
from pip._internal.req.req_set import RequirementSet


def get_supported_wheels(wheel_directory):
    requirement_set = RequirementSet()
    for f in os.listdir(wheel_directory):
        wheel_filename = os.path.join(wheel_directory, f)

        requirement = install_req_from_line(wheel_filename)
        requirement.is_direct = True

        try:
            requirement_set.add_requirement(requirement)
        except InstallationError:
            # This deliberately filters out incompatible requirements.
            pass

    return [req.link.path for req in requirement_set.requirements.values()]


def find_wsgi_py(search_root):
    for root, dirnames, filenames in os.walk(search_root):
        if 'wsgi.py' in filenames:
            return os.path.join(root, 'wsgi.py')


def setup_virtualenv():
    extract_location = os.path.realpath(os.path.dirname(__file__))

    # If there's a wsgi.py file in the deployed code, create a symlink for it
    # from the root. This makes it easier to target using Apache.
    wsgi_py_filename = find_wsgi_py(extract_location)

    if wsgi_py_filename:
        os.symlink(wsgi_py_filename, os.path.join(extract_location, 'wsgi.py'))

    # Identify this virtual environment's site-packages. At this point before
    # any packages have been installed, this will always be the last entry in
    # the Python path.
    site_packages = sys.path[-1]

    # Install project dependencies from the remaining wheels in the zipfile,
    # but only those that are compatible with the current version of Python.
    wheel_directory = os.path.join(extract_location, 'wheels')
    supported_wheel_filenames = get_supported_wheels(wheel_directory)

    # Install the compatible wheels.
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        'install',
        '--no-deps',
    ] + supported_wheel_filenames)

    # Copy .pth files into the virtual environment site-packages so that they
    # they get processed on Python startup.
    for pth_file in glob('%s/*.pth' % extract_location):
        shutil.copy(pth_file, site_packages)

    # Also copy the loadenv.py script to support automatic loading of
    # environment variables.
    shutil.copy(os.path.join(extract_location, 'loadenv.py'), site_packages)


if __name__ == '__main__':  # pragma: no cover
    setup_virtualenv()
