#!/bin/sh

set -e

# As CentOS is now EOL, certain package URLs no longer resolve properly.
# Run this script prior to "yum install".
# See https://serverfault.com/q/1161816.

sed -i s/mirror.centos.org/vault.centos.org/g /etc/yum.repos.d/CentOS-*.repo
sed -i s/^#.*baseurl=http/baseurl=http/g /etc/yum.repos.d/CentOS-*.repo
sed -i s/^mirrorlist=http/#mirrorlist=http/g /etc/yum.repos.d/CentOS-*.repo
