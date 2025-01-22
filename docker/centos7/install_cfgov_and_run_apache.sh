#!/usr/bin/env bash

# Fail when any command fails.
set -e

build_artifact="/cfgov/cfgov_current_build.zip"
cfgov_root=/srv/cfgov
install_location="$cfgov_root/current"
cfgov_environ="$install_location/environment.json"
cfgov_httpd="$install_location/cfgov/apache"
system_httpd=/opt/rh/httpd24

# Verify that the artifact is where we expect it to be.
if [[ ! -e "$build_artifact" ]]; then
    echo "Build artifact $build_artifact does not exist." >&2
    echo "Did you forget to mount the Docker volume?" >&2
    exit 1
fi

# Create directory for unpacked artifact.
mkdir -p "$install_location"

# Create staticfiles directory.
# TODO: Remove along with Apache conf, this is no longer used.
mkdir -p "$cfgov_root/static"

# Activate the appropriate version of Python and unpack the artifact.
. /opt/rh/rh-python38/enable
python "$build_artifact" -d "$install_location"

# Patch SQLite with a newer version.
# The version that comes with CentOS 7/Python 3.8 is 3.7.17.
# As of Django 2.2, the minimum supported SQLite version is 3.8.3:
# https://docs.djangoproject.com/en/2.2/releases/2.2/#miscellaneous
# This hack patches Python to use the newer pysqlite3 version instead.
"$install_location/venv/bin/pip" install --no-cache-dir pysqlite3-binary
echo \
    'import pysqlite3;'\
    'import sys;' \
    'sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")' > \
    "$install_location/venv/lib/python3.8/site-packages/patch_sqlite.pth"

# Create Django environment JSON file from the environment.
echo "{" > "$cfgov_environ"
env | sort | sed 's/\(.*\)=\(.*\)/  "\1": "\2",/' >> "$cfgov_environ"
sed -i '$ s/,$/\n}/' "$cfgov_environ"

# Collect Django static files.
"$install_location/venv/bin/django-admin" collectstatic --noinput

# Migrate and populate the Django database.
"$install_location/venv/bin/django-admin" migrate --noinput
"$install_location/venv/bin/django-admin" createcachetable
"$install_location/venv/bin/django-admin" runscript initial_data

# Create necessary Apache symlinks.
for symlink in modules run; do
    ln -s "$system_httpd/root/etc/httpd/$symlink" "$cfgov_httpd/$symlink"
done
ln -s "$cfgov_httpd/conf.d/wsgi.conf.venv" "$cfgov_httpd/conf.d/wsgi.conf"

# Give the Apache user permission to read the unpacked files.
chown -R "$APACHE_USER":"$APACHE_GROUP" "$cfgov_root"

# Run Apache the way the systemd service would.
# See /usr/lib/systemd/system/httpd24-httpd.service.
. "$system_httpd/enable"
set -a
. "$system_httpd/root/etc/sysconfig/httpd"
"$system_httpd/root/usr/sbin/httpd" \
    -f /srv/cfgov/current/cfgov/apache/conf/httpd.conf \
    -DFOREGROUND
