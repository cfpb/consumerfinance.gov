#!/bin/sh

# Set script to exit on any errors.
set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $DIR/test_processors.py
