source /src/cfgov-refresh/.env
source /etc/profile.d/extend-environment.sh
rm /src/cfgov-refresh/cfgov/apache/modules 2>/dev/null
ln -s /etc/httpd/modules /src/cfgov-refresh/cfgov/apache
/etc/profile.d/alias-static.sh
httpd -f /src/cfgov-refresh/cfgov/apache/conf/httpd.conf -D FOREGROUND
