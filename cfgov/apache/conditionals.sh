#!/bin/bash

# Some servers redirect /f/ to s3, others alias
# to a local path
if [[ "$APACHE_UPLOADS_F_ALIAS" =~ "http" ]] ; then
  echo "Redirect /f/ $APACHE_UPLOADS_F_ALIAS"
else
  echo "Alias /f/ $APACHE_UPLOADS_F_ALIAS"
fi

if ! [ -z "$APACHE_HTTPS_FORWARDED_HOST" ] ; then
  echo "RequestHeader set X-Forwarded-Proto https"
  echo "RequestHeader set X-Forwarded-Host $APACHE_HTTPS_FORWARDED_HOST"
fi

if ! [ -z "$APACHE_COMMON_LOGIN_ALIAS" ] ; then
  echo "Redirect /common/login /django-admin/login"
fi
