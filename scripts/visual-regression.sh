#!/bin/bash
# Create base images off the `main` branch for visual regression testing.

# Create variable for the current branch name.
branch=$(git symbolic-ref --short HEAD)

# Stash any changes on the current working branch.
git stash

# Checkout the `main` branch.
git checkout main

# Build assets.
yarn build

# Create variable for the screenshots path.
screenshots="test/cypress/visual-regression/base"

# Create variable for spec pattern.
specpattern="test/cypress/integration/layouts/*.cy.js"

# Generate base images.
./node_modules/.bin/cypress run \
    --env type=base \
    --config \
        screenshotsFolder=\"$screenshots\",specPattern=\"$specpattern\"

# Return to the working branch.
git checkout $branch

# Stash any changes on the current working branch.
git stash pop

# Re-build assets.
yarn build

yarn cypress run --spec "$specpattern"
