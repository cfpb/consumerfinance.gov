#!/bin/sh

# run npm install if node_modules doesn exist, or if it is older than
# packages.json
if [ ! -d node_modules ] ||  [ "packages.json" -nt node_modules ];
	then
	npm install
fi
gulp build
gulp watch
