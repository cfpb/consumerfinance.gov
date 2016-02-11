#!/bin/sh

# ==========================================================================
# Setup script for MYSQL Databse Instantiation
# NOTE: Run this script while in the project root directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Functions
ok() { echo -e $1; }

EXPECTED_ARGS=3
E_BADARGS=65
MYSQL=`which mysql`

if [ -z "$1" ] && [ -z "$2" ] && [ -z "$3" ]
then
  Q1="CREATE DATABASE IF NOT EXISTS v1;"
  Q2="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '';"
  Q3="FLUSH PRIVILEGES;"
  SQL="${Q1}${Q2}${Q3}"

  $MYSQL -uroot -e "$SQL"
  echo "Database v1 and user root created with a blank password"
else
  Q1="CREATE DATABASE IF NOT EXISTS $1;"
  Q2="GRANT ALL ON *.* TO '$2'@'localhost' IDENTIFIED BY '$3';"
  Q3="FLUSH PRIVILEGES;"
  SQL="${Q1}${Q2}${Q3}"


  if [ $# -ne $EXPECTED_ARGS ]
  then
    echo "Usage: $0 dbname dbuser dbpass"
    exit $E_BADARGS
  fi

  $MYSQL -uroot -e "$SQL"
  ok "Database $1 and user $2 created with a password $3"
fi





