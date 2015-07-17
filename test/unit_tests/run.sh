#!/bin/sh

# Set script to exit on any errors.
set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
#echo $DIR;

for d in $DIR/modules/*
do
  mocha $d --reporter=nyan;
done
