#!/usr/bin/env bash

FONT_VARIABLE="source-sans-3-latin-wght-normal.woff2"
BASE_DIR="./static.in/cfgov-fonts/fonts"

# Add required webfonts locally to docs/fonts/ directory.
mkdir $BASE_DIR
echo "Copying ./node_modules/@fontsource-variable/source-sans-3/files/$FONT_VARIABLE to $BASE_DIR/$FONT_VARIABLE"
cp ./node_modules/@fontsource-variable/source-sans-3/files/$FONT_VARIABLE $BASE_DIR/$FONT_VARIABLE
