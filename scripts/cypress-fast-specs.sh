#!/bin/bash
# Used by `yarn cy fast` command.
echo -n "${CHANGED_FILES:-$(git --no-pager diff --name-only origin/main)}" \
  | sed 's/___/\n/g' \
  | node "$(git rev-parse --show-toplevel)/test/cypress/spec-map.js"
