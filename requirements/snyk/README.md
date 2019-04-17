# Requirements files for Snyk

The files in the subdirectories of this one are symlinks back to the original
requirements files in the main `requirements/` directory
(this directory's parent).
They are needed for the current version of the Snyk.io service
to be able to check the requirements, since (as of March 6, 2019) it
can only check files named exactly `requirements.txt` and it
cannot follow `-r` references to other requirements files.

[This symlink-based setup was suggested by a Snyk maintainer](https://github.com/snyk/snyk-python-plugin/issues/21#issuecomment-463514410)
as a workaround until they add those features to their service.
