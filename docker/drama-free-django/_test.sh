#!/usr/bin/env bash

# Fail when any command fails.
set -e

artifact_filename=cfgov_current_build.zip
artifact_volume=/cfgov

# Verify that the artifact volume has been mapped.
if [ ! -d "$artifact_volume" ]; then
    echo "Artifact directory $artifact_volume does not exist."
    echo "Did you forget to mount the Docker volume?"
    exit 1
fi

# Install runtime requirements.
yum install -y centos-release-scl
yum install -y python27

source /opt/rh/python27/enable

# Extract the artifact in /tmp.
cp "$artifact_volume/$artifact_filename" /tmp
cd /tmp
python "./$artifact_filename"

cd current

export ALLOWED_HOSTS=[]
export DJANGO_SETTINGS_MODULE=cfgov.settings.production

# We want to test collectstatic, but we might not have webfont files if this
# script is running somewhere public like on Travis CI. Because cfgov-refresh
# uses the Django ManifestStaticFilesStorage backend, the collectstatic command
# will fail if any referenced files are missing.
#
# Builds generated with webfont files place them in a static.in/0/fonts
# subdirectory. Builds generated without these files don't have this directory.
#
# If we don't have the webfont files, we create empty files with the same name
# to allow collectstatic to run successfully. If the files already exist, these
# commands do nothing.
mkdir -p static.in/0/fonts

# 1. Use grep to find all .woff and .woff2 files referenced in CSS files.
# 2. Reduce these to a list of unique webfont filenames.
# 3. Touch each filename in static.in/0/fonts, causing it to be created as an
# empty file if it doesn't exist already.
grep -Eho \
    '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}.woff2?' \
    cfgov/static_built/css/*.css \
    | sort \
    | uniq \
    | sed 's|^|static.in/0/fonts/|' \
    | xargs touch

# Now that we're sure that we have webfont files, we can test collectstatic.
./venv/bin/django-admin collectstatic

# It'd be nice to do additional verification of the build artifact here, for
# example by actually running a webserver and making some requests.
