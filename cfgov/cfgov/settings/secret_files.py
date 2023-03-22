import logging
import os
from pathlib import Path
from typing import Union


logger = logging.getLogger(__name__)


def load_secret_files(secrets_dir: Union[Path, str] = None) -> None:
    """
    Load secrets from the specified directory (recursively), using the
    filename as runtime environment variables with their values set
    to the contents of the file (newline is stripped). These can
    then be accessed from `os.environ` or `os.getenv` during Python
    runtime after calling this function.
    :param secrets_dir: Path like object (Path or str), default is
    `SECRETS_DIR` environment variable value, or `/var/run/secrets` if
    the environment variable is undefined.
    :type secrets_dir: Path | str
    :return: None
    """
    if secrets_dir is None:
        logger.debug(
            "secrets_dir undefined. Using SECRETS_DIR "
            "or default to /var/run/secrets/cfgov"
        )
        secrets_dir = os.getenv("SECRETS_DIR", "/var/run/secrets/cfgov")
    logger.debug(f"secrets_dir: {secrets_dir}")
    if not os.path.isdir(secrets_dir):
        logger.warning(f"{secrets_dir} is not a directory! Soft Abort!")
        return
    for root, _, files in os.walk(secrets_dir):
        for file in files:
            logger.debug(f"Detected {os.path.join(root, file)}")
            # Ignore SECRETS_FOLLOW_SYMLINKS file (security).
            # If SECRETS_FOLLOW_SYMLINKS is set as an actual var,
            # and it is true, then "follow" (open) the symlink.
            # This is not secure to use in production!!!
            if file.upper() == "SECRETS_FOLLOW_SYMLINKS" or (
                os.getenv("SECRETS_FOLLOW_SYMLINKS", "").lower() != "true"
                and os.path.islink(os.path.join(root, file))
            ):
                logger.debug(
                    f"{file} is symlink "
                    f"(or SECRETS_FOLLOW_SYMLINKS) and ignoring!"
                )
                continue
            logger.debug(
                f"Loading secret {file} from {os.path.join(root, file)}."
            )
            with open(os.path.join(root, file)) as f:
                os.environ[file] = f.read().strip()
            logger.debug(f"Loaded secret {file}.")
