#!/bin/bash

project_name=${PWD##*/}
ret=0

if ! grep $project_name README.md 1>/dev/null; then
    echo "$project_name was not found in README.md"
    ret=1
fi

required_files=('CONTRIBUTING.md' 'COPYING.txt' 'README.md' 'TERMS.md')

for file in "${required_files[@]}"; do
    if [ ! -f $file ]; then
        echo "Required File: $file not found"
        ret=1
    fi
done

exit $ret
