#!/bin/sh

# Set script to exit on any errors.
set -e

TEST_DIR="test/"*
for d in $TEST_DIR
do
  if [ "$d" != "test/unit_test_coverage" ];
    then
      $d"/run.sh";
  fi
done
