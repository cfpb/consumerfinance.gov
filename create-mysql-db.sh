#!/bin/sh

# ==========================================================================
# Setup script for MySQL database instantiation—used to create the database.
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
  Q1="CREATE DATABASE IF NOT EXISTS $MYSQL_NAME;"
  Q2="GRANT ALL ON *.* TO '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '';"
  Q3="FLUSH PRIVILEGES;"
  SQL="${Q1}${Q2}${Q3}"

  $MYSQL -uroot -e "$SQL"
  echo "Database $MYSQL_NAME and user $MYSQL_USER created with a blank password"
else
  Q1="CREATE DATABASE IF NOT EXISTS $1;"
  Q2="GRANT ALL ON *.* TO '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '$MYSQL_PW';"
  Q3="FLUSH PRIVILEGES;"
  SQL="${Q1}${Q2}${Q3}"


  if [ $# -ne $EXPECTED_ARGS ]
  then
    echo "Usage: $0 dbname"
    exit $E_BADARGS
  fi

  $MYSQL -uroot -e "$SQL"
  ok "Database $1 and user $MYSQL_USER created with a password $MYSQL_PW"
fi
