#!/bin/sh

if [ -f /src/pdfreactor_key.txt ]; then
    export PDFREACTOR_LICENSE=`cat /src/pdfreactor_key.txt`
fi
mysqladmin -h $MYSQL_HOST create v1 || true
scl enable python27 "django-admin migrate --fake-initial --noinput"
scl enable python27 "django-admin runserver 0.0.0.0:8000"
