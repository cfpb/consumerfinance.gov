FROM httpd:2.4.65-alpine

# Define default Apache ENV variables.
ENV APACHE_PORT="8080"
ENV APACHE_USER="www-data"
ENV APACHE_GROUP="www-data"
ENV APACHE_SERVER_ROOT="/usr/local/apache2"
ENV APACHE_UPLOADS_F_ALIAS="/src/consumerfinance.gov/cfgov/f/"
ENV STATIC_PATH="/usr/local/apache2/htdocs"
ENV ERROR_LOG="/proc/self/fd/2"
ENV ACCESS_LOG="/proc/self/fd/1"
ENV LIMIT_REQUEST_BODY="0"
ENV APACHE_STATUS_ALLOW_FROM="127.0.0.1"

# Copy Apache configuration files.
COPY ./conf "$APACHE_SERVER_ROOT/conf"
COPY ./conf.d "$APACHE_SERVER_ROOT/conf.d"
COPY ./conf.modules.d "$APACHE_SERVER_ROOT/conf.modules.d"

# Delete default Apache homepage.
RUN rm -f "$APACHE_SERVER_ROOT/htdocs/index.html"

# The default httpd image runs as root but we want to run as the www-data user.
# This user doesn't have permission for $APACHE_SERVER_ROOT/logs, which is
# where Apache writes its pidfile. Even though we don't write logs here (since
# we redirect both ACCESS_LOG and ERROR_LOG below), we still need to give
# the www-data user acccess to this directory.
RUN mkdir -p "$APACHE_SERVER_ROOT/logs" \
    && chown www-data:www-data "$APACHE_SERVER_ROOT/logs"

EXPOSE 8080

USER www-data

CMD ["httpd-foreground"]
