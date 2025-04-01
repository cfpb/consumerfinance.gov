#!/bin/sh

if [ "$1" = "fast" ]; then
    ./scripts/cypress-fast-specs.sh && ./node_modules/.bin/cypress run
elif [ "$1" = "open" ]; then
    ./node_modules/.bin/cypress open --config-file cypress.template.mjs
else
    ./node_modules/.bin/cypress run --config-file cypress.template.mjs $@
fi
