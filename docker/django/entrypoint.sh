#!/bin/sh

scl enable python27 "django-admin migrate --fake-initial --noinput"
scl enable python27 "django-admin runserver"
