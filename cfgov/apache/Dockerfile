FROM httpd:2.4-alpine

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
ENV APACHE_PROCESS_COUNT="4"

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

# libxml2 versions below 2.13.4-r5 suffer from HIGH CVE-2025-27113:
# https://nvd.nist.gov/vuln/detail/CVE-2025-27113
# Upstream httpd:2.4-alpine includes 2.13.4-r3 (at the time this image is
# being tested). This may be fixed upstream in future. Until then, we can
# upgrade to a newer fixed version from Alpine edge.
RUN CURRENT_LIBXML2=$( \
        apk version --no-cache libxml2 | \
        grep "^libxml2" | \
        awk '{print $1}' | \
        cut -d '-' -f2- \
    ) && \
    TARGET_LIBXML2="2.13.4-r5" && \
    LOWEST_LIBXML2=$( \
        printf '%s\n' "$CURRENT_LIBXML2" "$TARGET_LIBXML2" | \
        sort -V | \
        head -n1 \
    ) && \
    if \
        [ "$LOWEST_LIBXML2" = "$CURRENT_LIBXML2" ] && \
        [ "$CURRENT_LIBXML2" != "$TARGET_LIBXML2" ] \
    ; then \
        echo "Patching libxml2 due to CVE-2025-27113 as $CURRENT_LIBXML2 < $TARGET_LIBXML2" && \
        echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories && \
        apk upgrade --no-cache libxml2; \
    fi

EXPOSE 8080

USER www-data

CMD ["httpd-foreground"]
