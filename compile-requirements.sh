#!/bin/bash

# ==========================================================================
# Compile full and hashed set of dependencies from requirements/*.in files
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

set -e

# Always use the latest pip
pip install -U pip

# Use a pinned version of pip-tools
pip install pip-tools==7.1.0

# Generate our requirements files in the order in which they reference each other:
pip-compile --generate-hashes --resolver=backtracking --rebuild -r requirements/deployment.in
pip-compile --generate-hashes --resolver=backtracking --rebuild -r requirements/test.in
pip-compile --generate-hashes --resolver=backtracking --rebuild -r requirements/scripts.in
pip-compile --generate-hashes --resolver=backtracking --rebuild -r requirements/dev.in
pip-compile --generate-hashes --resolver=backtracking --rebuild -r requirements/docs.in
