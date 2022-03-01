#!/usr/bin/env python3

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from string import Template


@contextmanager
def temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def save_wheels(python_executable, destination, *args):
    """Collect Python wheels for all packages and requirements.

    Given a list of packages and requirements files, invoke "pip wheel" to
    download and/or create wheels for each of them, storing them in the
    specified destination directory.

    Call pip externally using this command:

        python -m pip wheel --wheel-dir=dest ...

    https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program
    """
    subprocess.check_call(
        [python_executable, "-m", "pip", "wheel"]
        + ["--wheel-dir=%s" % destination]
        + ["--find-links=%s" % destination]
        + list(args)
    )


def create_project_pth_file(project_name, target_directory):
    project_pth_template_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "project-name.pth.tmpl"
    )

    with open(project_pth_template_filename) as f:
        project_pth_template = Template(f.read())

    project_pth = project_pth_template.substitute(project_name=project_name)

    project_pth_filename = os.path.join(target_directory, "%s.pth" % project_name)

    with open(project_pth_filename, "w") as f:
        f.write(project_pth)


def create_zipfile(
    project_path,
    requirements_file,
    zipfile_basename,
    extra_static,
    extra_python,
):
    with temp_directory() as temp_dir:
        # Bootstrap wheels get stored in the zip under /bootstrap_wheels/.
        bootstrap_wheel_dir = os.path.join(temp_dir, "bootstrap_wheels")
        save_wheels(sys.executable, bootstrap_wheel_dir, "pip", "setuptools")

        # Other wheels get stored in the zip under /wheels/.
        wheel_dir = os.path.join(temp_dir, "wheels")

        wheel_executables = [sys.executable]
        if extra_python:
            wheel_executables.append(extra_python)

        for wheel_executable in wheel_executables:
            save_wheels(wheel_executable, wheel_dir, "-r%s" % requirements_file)

        # Copy the project code into the zip.
        project_name = os.path.basename(os.path.realpath(project_path))
        project_dir = os.path.join(temp_dir, project_name)

        shutil.copytree(project_path, project_dir)

        # Create a .pth file that will add the project code to the Python path.
        create_project_pth_file(project_name, temp_dir)

        # Copy a .pth file and script to support the automatic loading of
        # environment variables upon Python startup.
        script_dir = os.path.dirname(os.path.realpath(__file__))

        shutil.copy(os.path.join(script_dir, "loadenv-init.pth"), temp_dir)
        shutil.copy(os.path.join(script_dir, "loadenv.py"), temp_dir)

        # Add scripts used to extract the zipfile.
        shutil.copyfile(
            os.path.join(script_dir, "extract.py"),
            os.path.join(temp_dir, "__main__.py"),
        )

        shutil.copy(os.path.join(script_dir, "install_wheels.py"), temp_dir)

        # Add any static file directories, if provided.
        for i, static_dir in enumerate(extra_static or []):
            shutil.copytree(static_dir, os.path.join(temp_dir, "static.in/%s/" % i))

        zipfile = shutil.make_archive(zipfile_basename, "zip", temp_dir)

        # Make zipfile executable, so that it can be executed directly
        # (./archive.zip ...) instead of having to invoke Python
        # (python ./archive.zip ...).
        #
        # This requires both prepending the file with the shebang
        # "#!/usr/bin/env/python", as well as making it executable, doing
        # the equivalent of "chmod +x archive.zip".
        with open(zipfile, "rb") as f:
            zipfile_data = f.read()

        with open(zipfile, "wb") as f:
            f.write(b"#!/usr/bin/env python\n")
            f.write(zipfile_data)

        existing_st_mode = os.stat(zipfile)[0]
        new_st_mode = existing_st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(zipfile, new_st_mode)

        return zipfile


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Create deployable zipfile for a Django project"
    )

    parser.add_argument("project_path")
    parser.add_argument("requirements_file")
    parser.add_argument("zipfile_basename")
    parser.add_argument(
        "--extra-static",
        action="append",
        help="Optionally include additional static file directories",
    )
    parser.add_argument(
        "--extra-python",
        help="Optionally build wheels for a second Python version",
    )

    args = parser.parse_args()

    create_zipfile(**vars(args))
