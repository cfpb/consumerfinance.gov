#!/bin/sh

echo "overwriting your node_modules with the versions built into this docker image"
/bin/cp -rf ../node_modules ./node_modules

gulp build
gulp watch
