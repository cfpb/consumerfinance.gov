#!/bin/bash

# Some servers redirect /f/ to s3, others alias
# to a local path
if [[ "$APACHE_UPLOADS_F_ALIAS" =~ "http" ]]
then
echo "Redirect /f/ $APACHE_UPLOADS_F_ALIAS
Redirect /wp-content/uploads/ $APACHE_UPLOADS_F_ALIAS"
else
echo "Alias /f/ $APACHE_UPLOADS_F_ALIAS
Alias /wp-content/uploads ${APACHE_WWW_PATH}/html/wordpress/wp-content/uploads
<Directory $APACHE_UPLOADS_F_ALIAS>
  Require all granted
</Directory>
<Directory ${APACHE_WWW_PATH}/html/wordpress/wp-content/uploads>
  Require all granted
</Directory>"
fi

if ! [ -z "$APACHE_HTTPS_FORWARDED_HOST" ]
then
echo "RequestHeader set X-Forwarded-Proto https
RequestHeader set X-Forwarded-Host $APACHE_HTTPS_FORWARDED_HOST"
fi

if ! [ -z "$APACHE_COMMON_LOGIN_ALIAS" ]
then
echo "Redirect /common/login /django-admin/login"
fi
