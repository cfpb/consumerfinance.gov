#!/bin/bash
cp -f cfgov/apache/conf.d/alias.tmpl cfgov/apache/conf.d/alias.conf
if [ ! -z ${DJANGO_SETTINGS_MODULE+x} ] && [ "$DJANGO_DEBUG" != "true" ]; then
  echo "Alias /static/ ${STATIC_PATH}" >> cfgov/apache/conf.d/alias.conf
fi
