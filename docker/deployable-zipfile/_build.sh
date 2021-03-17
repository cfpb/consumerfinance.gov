#!/usr/bin/env bash

# Fail when any command fails.
set -e

# Echo commands.
set -x

# Set GIT_COMMITTER_NAME to enable us to `pip -e` from git URLs
# git < 2.6.5 requires either these variables to be set or the user to exist 
# in passwd file.
export GIT_COMMITTER_NAME="cf.gov build user"
export GIT_COMMITTER_EMAIL="tech@cfpb.gov"

build_artifact_name=cfgov_current_build
build_artifact="$build_artifact_name.zip"
cfgov_refresh_volume=/cfgov
webfonts_path="$cfgov_refresh_volume/static.in/cfgov-fonts"

# Verify that the source volume has been mapped.
if [ ! -d "$cfgov_refresh_volume" ]; then
    echo "Source directory $cfgov_refresh_volume does not exist."
    echo "Did you forget to mount the Docker volume?"
    exit 1
fi

# Run the frontend build.
pushd "$cfgov_refresh_volume"
./frontend.sh production
popd

# Prepare arguments for the deployable zipfile build.
build_args=(
    "$cfgov_refresh_volume/cfgov"
    "$cfgov_refresh_volume/requirements/deployment.txt"
    "$build_artifact_name"
)

if [ -d "$webfonts_path" ]; then
    build_args+=("--extra-static" "$webfonts_path")
fi

# Build the deployable zipfile.
"$cfgov_refresh_volume/cfgov/deployable_zipfile/create.py" "${build_args[@]}"

# Copy build artifact to source directory.
cp "$build_artifact" "$cfgov_refresh_volume"
echo "Generated $build_artifact in $cfgov_refresh_volume."
