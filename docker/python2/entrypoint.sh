source /src/cfgov-refresh/.env
source /etc/profile.d/extend-environment.sh
rm /src/cfgov-refresh/apache/modules 2>/dev/null
ln -s /etc/httpd/modules /src/cfgov-refresh/apache
httpd -f /src/cfgov-refresh/apache/conf/httpd.conf -D FOREGROUND
