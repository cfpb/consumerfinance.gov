#!/bin/sh

if [ -f /src/pdfreactor_key.txt ]; then
    export PDFREACTOR_LICENSE=`cat /src/pdfreactor_key.txt`
fi
if [ -f /src/mapbox_key.txt ]; then
    export MAPBOX_ACCESS_TOKEN=`cat /src/mapbox_key.txt`
fi
for d in /src/develop-apps/*/ ; do
        export PYTHONPATH=$d:$PYTHONPATH
done
mysqladmin -h $MYSQL_HOST create v1 || true
scl enable python27 "django-admin migrate --fake-initial --noinput"
scl enable python27 "django-admin runserver 0.0.0.0:8000"
