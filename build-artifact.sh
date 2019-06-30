#!/bin/bash

# exit when any command fails
set -e -x

# some of these are poorly named.
SLUG=${1:-demo}
PORT=${2:-8000}
TMP_DIR=$(mktemp -d -t cfgov-$SLUG-XXXXXXXXXX)
SERVER_HTML_PATH=/etc/cfgov-apache/htdocs
SERVER_STATIC_PATH=${SERVER_HTML_PATH}/static-$SLUG
RELATIVE_APP_DESTINATION=/srv/cfgov/$SLUG
APP_DESTINATION=${TMP_DIR}${RELATIVE_APP_DESTINATION}
STATIC_DESTINATION=${TMP_DIR}${SERVER_HTML_PATH}
DJANGO_STATIC_ROOT=$STATIC_DESTINATION/static-$SLUG

# setup directories, create virtualenv, copy files
mkdir -p $APP_DESTINATION/static.in
virtualenv $APP_DESTINATION/venv 
cp -r cfgov $APP_DESTINATION/cfgov
rm -rf $APP_DESTINATION/cfgov/unprocessed
cp -r cfgov/apache/conf.d $APP_DESTINATION/conf.d

# install dependencies into the virtualenv
$APP_DESTINATION/venv/bin/pip install -r /src/cfgov-refresh/requirements/deployment.txt
$APP_DESTINATION/venv/bin/pip install -r /src/cfgov-refresh/requirements/optional-public.txt
DJANGO_STATIC_ROOT=$STATIC_DESTINATION/static-$SLUG \
	ALLOWED_HOSTS='["*"]' \
       	PYTHONPATH=$APP_DESTINATION/cfgov \
	DJANGO_SETTINGS_MODULE=cfgov.settings.minimal_collectstatic \
       	  $APP_DESTINATION/venv/bin/django-admin collectstatic

# There should only ever be one site-packages in a virtualenv.
# Looping through "them" is a shortcut around the need to figure out
# where we need to write the pth file
#
# The end result, is when you run code in this virtualenv, the 'cfgov' 
# directory will be in the PYTHONPATH.
for site_packages in $APP_DESTINATION/venv/lib/*/site-packages
	do
		echo $RELATIVE_APP_DESTINATION/cfgov > $site_packages/cfgov.pth
	done

# entrypoint.py is a simple wrapper around cfgov.wsgi, that
# sets DJANGO_STATIC_ROOT. As far as I can tell, DJANGO_STATIC_ROOT
# is unique as a *deployment-specific* variable.
cat << EOF > $APP_DESTINATION/entrypoint.py
import os
os.environ['DJANGO_STATIC_ROOT']='$SERVER_STATIC_PATH'
from cfgov.wsgi import application
EOF

# This is how we add our other Apache configurations. See
# how inlude.conf is passed in below as part of activate.sh
cat << EOF > $APP_DESTINATION/include.conf
Define APACHE_WWW_PATH $SERVER_HTML_PATH
Define STATIC_PATH $SERVER_STATIC_PATH
Define CFGOV_SANDBOX $SERVER_HTML_PATHsandbox
LoadModule expires_module \${MOD_WSGI_MODULES_DIRECTORY}/mod_expires.so
LoadModule substitute_module \${MOD_WSGI_MODULES_DIRECTORY}/mod_substitute.so
Include "/srv/cfgov/$SLUG/conf.d/*.conf"
EOF


# activate.sh runs  mod_wsgi-express setup-server with all of the configuration
# we need to run the app. The result is some apache configuration written
# to /etc/cfgov-apache
cat << EOF > $APP_DESTINATION/activate.sh
$RELATIVE_APP_DESTINATION/venv/bin/mod_wsgi-express setup-server \
 --port $PORT --user apache --group apache\
 --server-root=/etc/cfgov-apache/ \
 $RELATIVE_APP_DESTINATION/entrypoint.py \
 --python-path $RELATIVE_APP_DESTINATION/cfgov/ \
 --python-path $RELATIVE_APP_DESTINATION/venv/lib/*/site-packages/ \
 --passenv MEDIA_ROOT \
 --passenv DJANGO_DEBUG \
 --passenv ADMIN_EMAILS \
 --passenv AKAMAI_OBJECT_ID \
 --passenv ALLOW_ADMIN_URL \
 --passenv AWS_ACCESS_KEY_ID \
 --passenv AWS_SECRET_ACCESS_KEY \
 --passenv AWS_S3_URL \
 --passenv AWS_S3_CUSTOM_DOMAIN \
 --passenv AWS_STORAGE_BUCKET_NAME \
 --passenv CSP_ENFORCE \
 --passenv CSP_REPORT \
 --passenv DATABASE_ROUTING \
 --passenv DEPLOY_ENVIRONMENT \
 --passenv ED_API_KEY \
 --passenv EMAIL_HOST \
 --passenv EMAIL_SUBJECT_PREFIX \
 --passenv ENABLE_AKAMAI_CACHE_PURGE \
 --passenv AKAMAI_ACCESS_TOKEN \
 --passenv AKAMAI_CLIENT_SECRET \
 --passenv AKAMAI_CLIENT_TOKEN \
 --passenv AKAMAI_FAST_PURGE_URL \
 --passenv AKAMAI_PURGE_ALL_URL \
 --passenv CLOUDFRONT_DISTRIBUTION_ID_FILES \
 --passenv ENABLE_CLOUDFRONT_CACHE_PURGE \
 --passenv ES_HOST \
 --passenv HTTPS_PROXY \
 --passenv HTTP_PROXY \
 --passenv LOGIN_FAILS_ALLOWED \
 --passenv LOGIN_FAIL_TIME_PERIOD \
 --passenv NO_PROXY \
 --passenv REGSGOV_BASE_URL \
 --passenv S3_ENABLED \
 --passenv SECRET_KEY \
 --passenv WAGTAILADMIN_NOTIFICATION_FROM_EMAIL \
 --passenv http_proxy \
 --passenv https_proxy \
 --passenv no_proxy \
 --passenv CCDB_UI_URL \
 --passenv COMPLAINT_ES_INDEX \
 --passenv COMPLAINT_DOC_TYPE \
 --passenv GITHUB_TOKEN \
 --passenv MATTERMOST_WEBHOOK_URL \
 --passenv SQS_QUEUE_ENABLED \
 --passenv AWS_SQS_ACCESS_KEY_ID \
 --passenv AWS_SQS_SECRET_ACCESS_KEY \
 --passenv AWS_SQS_QUEUE_URL \
 --passenv SHEER_ELASTICSEARCH_INDEX \
 --passenv ALLOWED_HOSTS \
 --passenv GOVDELIVERY_BASE_URL \
 --passenv GOVDELIVERY_USER \
 --passenv GOVDELIVERY_PASSWORD \
 --passenv USE_X_FORWARDED_PORT \
 --passenv NEW_RELIC_APP_NAME \
 --passenv NEW_RELIC_LICENSE_KEY \
 --passenv NEW_RELIC_LOG \
 --passenv DATABASE_URL \
 --passenv DJANGO_SETTINGS_MODULE \
 --passenv ENABLE_DEFAULT_FRAGMENT_CACHE \
 --passenv EREGS_API_BASE \
 --passenv ES_PORT \
 --passenv GITHUB_REPO \
 --passenv GITHUB_URL \
 --passenv GITHUB_USER \
 --passenv GOVDELIVERY_ACCOUNT_CODE \
 --passenv MAPBOX_ACCESS_TOKEN \
 --passenv MATTERMOST_USERNAME \
 --passenv PGPASSWORD \
 --passenv REGSGOV_API_KEY \
 --passenv SUBSCRIPTION_SERVER_ERROR_URL \
 --passenv SUBSCRIPTION_SUCCESS_URL \
 --passenv SUBSCRIPTION_USER_ERROR_URL \
 --setenv DJANGO_STATIC_ROOT $SERVER_STATIC_PATH \
 --include-file $RELATIVE_APP_DESTINATION/include.conf \
 --url-alias /static $SERVER_STATIC_PATH
EOF

chmod +x $APP_DESTINATION/activate.sh

find $APP_DESTINATION/venv/bin -maxdepth 1 -type f -exec sed -i "s@$APP_DESTINATION/venv@$RELATIVE_APP_DESTINATION/venv@g" {} \;

mkdir -p /src/cfgov-refresh/build
cd $TMP_DIR && tar -czvf /src/cfgov-refresh/build/$SLUG.tgz . --owner=apache --group=apache
rm -rf $TMP_DIR
