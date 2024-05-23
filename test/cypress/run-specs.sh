#!/bin/bash
echo -n "${CHANGED_FILES:-$(git --no-pager diff --name-only origin/main)}" \
  | tr -s "___" "\n" \
  | node "$(git rev-parse --show-toplevel)/test/cypress/spec-map.js"
