#!/bin/sh

# ==========================================================================
# Setup script used to drop MySQL database.
# NOTE: Run this script while in the project root directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Functions
ok() { echo -e $1; }

EXPECTED_ARGS=1
E_BADARGS=65
MYSQL=`which mysql`

if [ -z "$1" ]
then
  Q1="drop database $MYSQL_NAME;"
  SQL="${Q1}"

  $MYSQL -uroot -e "$SQL"
  echo "Database $MYSQL_NAME dropped."
else
  Q1="drop database $1;"
  SQL="${Q1}"

  if [ $# -ne $EXPECTED_ARGS ]
  then
    echo "Usage: $0 dbname"
    exit $E_BADARGS
  fi

  $MYSQL -uroot -e "$SQL"
  ok "Database $1 dropped."
fi
