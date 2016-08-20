#!/bin/sh

scl enable python27 "django-admin migrate --fake-inital --noinput"
scl enable python27 "django-admin runserver"
