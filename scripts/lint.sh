#!/bin/sh

# Exit on error from any of the linting sub-tasks.
set -e

## Run prettier. See ignored path in .prettierignore.
yarn prettier "./**/*.{js,jsx,ts,tsx,md,css,scss}" --write

## Run JS linting. See ignored path in .eslintignore.
eslint "./{cfgov/unprocessed,config,esbuild,scripts,test}/**/*.js" --fix

## Run CSS linting. See ignored path in .stylelintignore.
stylelint "./cfgov/unprocessed/**/*.{css,scss}" --fix
