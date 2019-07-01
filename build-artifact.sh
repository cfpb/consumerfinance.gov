#!/bin/bash

# exit when any command fails
set -e -x

# some of these are poorly named.
SLUG=${1:-demo}
PORT=${2:-8000}
TMP_DIR=$(mktemp -d -t cfgov-$SLUG-XXXXXXXXXX)
DESTINATION_ROOT=/srv/cfgov/$SLUG
DESTINATION_STATIC=/srv/cfgov/$SLUG/static
STAGING_ROOT=${TMP_DIR}/$SLUG
STAGING_STATIC=${TMP_DIR}/$SLUG/static

# setup directories, create virtualenv, copy files
virtualenv $STAGING_ROOT/venv 
cp -r cfgov $STAGING_ROOT/cfgov
rm -rf $STAGING_ROOT/cfgov/unprocessed
cp -r cfgov/apache/conf.d $STAGING_ROOT/conf.d

# install dependencies into the virtualenv
$STAGING_ROOT/venv/bin/pip install -r /src/cfgov-refresh/requirements/deployment.txt \
	                           -r /src/cfgov-refresh/requirements/optional-public.txt

# collect static files
DJANGO_STATIC_ROOT=$STAGING_STATIC \
	ALLOWED_HOSTS='["*"]' \
       	PYTHONPATH=$STAGING_ROOT/cfgov \
	DJANGO_SETTINGS_MODULE=cfgov.settings.minimal_collectstatic \
       	  $STAGING_ROOT/venv/bin/django-admin collectstatic

# There should only ever be one site-packages in a virtualenv.
# Looping through "them" is a shortcut around the need to figure out
# where we need to write the pth file
#
# The end result, is when you run code in this virtualenv, the 'cfgov' 
# directory will be in the PYTHONPATH.
for site_packages in $STAGING_ROOT/venv/lib/*/site-packages
	do
		echo $DESTINATION_ROOT/cfgov > $site_packages/cfgov.pth
	done

# entrypoint.py is a simple wrapper around cfgov.wsgi, that
# sets DJANGO_STATIC_ROOT. As far as I can tell, DJANGO_STATIC_ROOT
# is unique as a *deployment-specific* variable. If there are
# others, they can go here.
cat << EOF > $STAGING_ROOT/entrypoint.py
import os
os.environ['DJANGO_STATIC_ROOT']='$DESTINATION_STATIC'
from cfgov.wsgi import application
EOF

# This is how we add our other Apache configurations. See
# how inlude.conf is passed in below as part of activate.sh
cat << EOF > $STAGING_ROOT/include.conf
Define APACHE_WWW_PATH /etc/cfgov-apache/htdocs
Define STATIC_PATH $DESTINATION_STATIC
Define CFGOV_SANDBOX $/etc/cfgov-apache/htdocs/sandbox
LoadModule expires_module \${MOD_WSGI_MODULES_DIRECTORY}/mod_expires.so
LoadModule substitute_module \${MOD_WSGI_MODULES_DIRECTORY}/mod_substitute.so
Include "/srv/cfgov/$SLUG/conf.d/*.conf"
EOF

# common mod_wsgi-express arguments, used for both start-server and setup-server
cat << EOF > $STAGING_ROOT/_common_mod_wsgi_args.sh
export COMMON_MOD_WSGI_ARGS=' 
 --port $PORT --user apache --group apache
 $DESTINATION_ROOT/entrypoint.py 
 --python-path $DESTINATION_ROOT/cfgov/ 
 --python-path $DESTINATION_ROOT/venv/lib/*/site-packages/ 
 --passenv MEDIA_ROOT 
 --passenv DJANGO_DEBUG 
 --passenv ADMIN_EMAILS 
 --passenv AKAMAI_OBJECT_ID 
 --passenv ALLOW_ADMIN_URL 
 --passenv AWS_ACCESS_KEY_ID 
 --passenv AWS_SECRET_ACCESS_KEY 
 --passenv AWS_S3_URL 
 --passenv AWS_S3_CUSTOM_DOMAIN 
 --passenv AWS_STORAGE_BUCKET_NAME 
 --passenv CSP_ENFORCE 
 --passenv CSP_REPORT 
 --passenv DATABASE_ROUTING 
 --passenv DEPLOY_ENVIRONMENT 
 --passenv ED_API_KEY 
 --passenv EMAIL_HOST 
 --passenv EMAIL_SUBJECT_PREFIX 
 --passenv ENABLE_AKAMAI_CACHE_PURGE 
 --passenv AKAMAI_ACCESS_TOKEN 
 --passenv AKAMAI_CLIENT_SECRET 
 --passenv AKAMAI_CLIENT_TOKEN 
 --passenv AKAMAI_FAST_PURGE_URL 
 --passenv AKAMAI_PURGE_ALL_URL 
 --passenv CLOUDFRONT_DISTRIBUTION_ID_FILES 
 --passenv ENABLE_CLOUDFRONT_CACHE_PURGE 
 --passenv ES_HOST 
 --passenv HTTPS_PROXY 
 --passenv HTTP_PROXY 
 --passenv LOGIN_FAILS_ALLOWED 
 --passenv LOGIN_FAIL_TIME_PERIOD 
 --passenv NO_PROXY 
 --passenv REGSGOV_BASE_URL 
 --passenv S3_ENABLED 
 --passenv SECRET_KEY 
 --passenv WAGTAILADMIN_NOTIFICATION_FROM_EMAIL 
 --passenv http_proxy 
 --passenv https_proxy 
 --passenv no_proxy 
 --passenv CCDB_UI_URL 
 --passenv COMPLAINT_ES_INDEX 
 --passenv COMPLAINT_DOC_TYPE 
 --passenv GITHUB_TOKEN 
 --passenv MATTERMOST_WEBHOOK_URL 
 --passenv SQS_QUEUE_ENABLED 
 --passenv AWS_SQS_ACCESS_KEY_ID 
 --passenv AWS_SQS_SECRET_ACCESS_KEY 
 --passenv AWS_SQS_QUEUE_URL 
 --passenv SHEER_ELASTICSEARCH_INDEX 
 --passenv ALLOWED_HOSTS 
 --passenv GOVDELIVERY_BASE_URL 
 --passenv GOVDELIVERY_USER 
 --passenv GOVDELIVERY_PASSWORD 
 --passenv USE_X_FORWARDED_PORT 
 --passenv NEW_RELIC_APP_NAME 
 --passenv NEW_RELIC_LICENSE_KEY 
 --passenv NEW_RELIC_LOG 
 --passenv DATABASE_URL 
 --passenv DJANGO_SETTINGS_MODULE 
 --passenv ENABLE_DEFAULT_FRAGMENT_CACHE 
 --passenv EREGS_API_BASE 
 --passenv ES_PORT 
 --passenv GITHUB_REPO 
 --passenv GITHUB_URL 
 --passenv GITHUB_USER 
 --passenv GOVDELIVERY_ACCOUNT_CODE 
 --passenv MAPBOX_ACCESS_TOKEN 
 --passenv MATTERMOST_USERNAME 
 --passenv PGPASSWORD 
 --passenv REGSGOV_API_KEY 
 --passenv SUBSCRIPTION_SERVER_ERROR_URL 
 --passenv SUBSCRIPTION_SUCCESS_URL 
 --passenv SUBSCRIPTION_USER_ERROR_URL 
 --include-file $DESTINATION_ROOT/include.conf 
 --url-alias /static $DESTINATION_STATIC
'
EOF

# activate.sh runs  mod_wsgi-express setup-server with all of the configuration
# we need to run the app. The result is some apache configuration written
# to /etc/cfgov-apache
cat << EOF > $STAGING_ROOT/activate.sh
#!/usr/bin/env bash
source $DESTINATION_ROOT/_common_mod_wsgi_args.sh
$DESTINATION_ROOT/venv/bin/mod_wsgi-express setup-server \
 $DESTINATION_ROOT/entrypoint.py  \$COMMON_MOD_WSGI_ARGS \
 --server-root=/etc/cfgov-apache/ 
EOF

# like activate.sh, but it starts the server immediately, runs in the
# foreground, logs to stdout, and writes nothing to /etc
cat << EOF > $STAGING_ROOT/foreground.sh
#!/usr/bin/env bash
source $DESTINATION_ROOT/_common_mod_wsgi_args.sh
$DESTINATION_ROOT/venv/bin/mod_wsgi-express start-server \
 $DESTINATION_ROOT/entrypoint.py  \$COMMON_MOD_WSGI_ARGS --log-to-terminal --access-log  --startup-log 
EOF

# provide a predicatable script location for running migrations for the most recently deployed version
cat <<EOF > $TMP_DIR/cfgov-migrate-next.sh
#!/usr/bin/env bash
$DESTINATION_ROOT/venv/bin/django-admin migrate
EOF

# provide a predicatable script location for activating the most recently deployed version
cat <<EOF > $TMP_DIR/cfgov-activate-next.sh
#!/usr/bin/env bash
$DESTINATION_ROOT/activate.sh
EOF

chmod +x $STAGING_ROOT/*.sh
chmod +x $TMP_DIR/*.sh

# update the scripts to use the correct (post-install) paths
find $STAGING_ROOT/venv/bin -maxdepth 1 -type f -exec sed -i "s@$STAGING_ROOT/venv@$DESTINATION_ROOT/venv@g" {} \;

# a place to put builds
mkdir -p /src/cfgov-refresh/build

# Package up the artifact, making sure owner and group are 'apache'
cd $TMP_DIR && tar -czvf /src/cfgov-refresh/build/$SLUG.tgz . --owner=apache --group=apache

# cleanup
rm -rf $TMP_DIR
