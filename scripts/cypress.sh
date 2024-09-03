#!/bin/sh

if [ ${1:-run} = "fast" ]; then
    ./test/cypress/run-specs.sh && ./node_modules/.bin/cypress run
elif [ ${1:-run} = "open" ]; then
    ./node_modules/.bin/cypress open --config-file cypress.template.mjs
else
    ./node_modules/.bin/cypress run --config-file cypress.template.mjs
fi
