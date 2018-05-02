#!/bin/bash

# ==========================================================================
# Wrapper script for refresh-data.sh that grants proper MySQL permissions.
# This script is only needed for MySQL dumps that require SUPER privileges.
# NOTE: Run this script while in the project root directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

MYSQL=`which mysql`

UPDATE="UPDATE mysql.user SET Super_Priv='Y' WHERE user='$MYSQL_USER'"
FLUSH="FLUSH PRIVILEGES"
SQL="$UPDATE;$FLUSH;"

$MYSQL -uroot --password=$MYSQL_ROOT_PW $MYSQL_NAME -e "$SQL"

./refresh-data.sh $@
