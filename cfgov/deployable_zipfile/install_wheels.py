import argparse
import os
import subprocess  # nosec
import sys


def install_wheels(wheel_directory):
    wheel_filenames = sorted(
        os.path.join(wheel_directory, f) for f in os.listdir(wheel_directory)
    )

    subprocess.check_call(  # nosec
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
        ]
        + wheel_filenames
    )


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Extract a deployable Django project zipfile"
    )

    parser.add_argument("wheel_directory")

    args = parser.parse_args()

    install_wheels(**vars(args))
