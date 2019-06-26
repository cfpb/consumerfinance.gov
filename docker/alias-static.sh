#!/bin/bash
if [ ! -z ${DJANGO_SETTINGS_MODULE+x} ] && [ "$DJANGO_DEBUG" != "true" ]; then
  echo "Alias /static/ ${STATIC_PATH}" >> cfgov/apache/conf.d/alias.conf
fi
