#!/bin/sh

# Set script to exit on any errors.
set -e

TEST_DIR="test/"*
for d in $TEST_DIR
do
  $d'/run.sh';
done
