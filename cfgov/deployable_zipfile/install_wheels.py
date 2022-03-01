import argparse
import os
import subprocess
import sys

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

    return sorted(req.link.path for req in requirement_set.requirements.values())


def install_wheels(wheel_directory):
    supported_wheel_filenames = get_supported_wheels(wheel_directory)

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
        ]
        + supported_wheel_filenames
    )


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Extract a deployable Django project zipfile"
    )

    parser.add_argument("wheel_directory")

    args = parser.parse_args()

    install_wheels(**vars(args))
