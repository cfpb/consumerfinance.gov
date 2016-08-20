#!/bin/sh

if [ -e node_modules ]
then 
    echo "overwriting your node_modules with the versions built into this docker image"
    rm -rf node_modules
fi 

/bin/cp -rf ../node_modules ./node_modules

gulp build
gulp watch
