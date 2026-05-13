#!/bin/sh
yarn list --depth=3 2>/dev/null | \
awk '$NF~/@[0-9]\.[0-9]\.[0-9]/ {print $NF}' | \
sort -u | \
sed -e 's/\//-/' -e 's/@\([0-9]\)/-\1/' -e 's/$/.tgz/' | \
while IFS= read -r f; do
  if [ ! -f ".yarn/cache/$f" ]; then
    if [ $f != "css-2.2.4.tgz" ]; then
       echo "🚨 Missing $f in npm cache.🚨"
    fi
  fi
done
