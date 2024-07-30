#!/bin/bash
echo 'Updating search indexes'
./cfgov/manage.py opensearch index --force rebuild
./cfgov/manage.py opensearch document --force --refresh --parallel index
