FROM python:3.8-alpine as base

# cfgov-dev is used for local development, as well as a base for frontend and prod.
FROM base AS cfgov-dev

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
ENV ENV /etc/profile

LABEL maintainer="tech@cfpb.gov"

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

ENV APP_HOME /src/consumerfinance.gov
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

# Install common OS packages
RUN apk update --no-cache && apk upgrade --no-cache
# .build-deps are required to build and test the application (pip, tox, etc.)
RUN apk add --no-cache --virtual .build-deps gcc gettext git libffi-dev musl-dev postgresql-dev
# .backend-deps and .frontend-deps are required to run the application
RUN apk add --no-cache --virtual .backend-deps bash curl postgresql
RUN apk add --no-cache --virtual .frontend-deps jpeg-dev nodejs yarn zlib-dev
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Disables pip cache. Reduces build time, and suppresses warnings when run as non-root.
# NOTE: MUST be after pip upgrade. Build fails otherwise due to bug in old pip.
ENV PIP_NO_CACHE_DIR true

# Install python requirements
COPY requirements requirements
RUN pip install -r requrements/local.txt -r requrements/deployment.txt

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "./cfgov/manage.py", "runserver", "0.0.0.0:8000"]

# Build Frontend Assets
FROM cfgov-dev as cfgov-build

ENV STATIC_PATH ${APP_HOME}/cfgov/static/
ENV PYTHONPATH ${APP_HOME}/cfgov

# Django Settings
ENV DJANGO_SETTINGS_MODULE cfgov.settings.production
ENV DJANGO_STATIC_ROOT ${STATIC_PATH}
ENV ALLOWED_HOSTS '["*"]'

# See .dockerignore for details on which files are included
COPY . .

# Build the front-end
RUN ./frontend.sh production && \
    cfgov/manage.py collectstatic && \
    yarn cache clean && \
    rm -rf node_modules npm-packages-offline-cache

# Build mod_wsgi against target Python version
FROM base as cfgov-mod-wsgi
WORKDIR /tmp
RUN apk add --no-cache --virtual .build-deps apache2-dev gcc make musl-dev
RUN wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.0.tar.gz -O mod_wsgi.tar.gz
RUN echo -n "0a6f380af854b85a3151e54a3c33b520c4a6e21a99bcad7ae5ddfbfe31a74b50  mod_wsgi.tar.gz" | sha256sum -c
RUN tar xvf mod_wsgi.tar.gz
RUN cd mod_wsgi* && ./configure && make install
RUN ls /usr/lib/apache2/mod_wsgi.so  # Ensure it compiled and is where it's expected
RUN apk del .build-deps
RUN rm -Rf /tmp/mod_wsgi*

# Production-like Apache-based image
FROM cfgov-dev as cfgov-prod

ENV HTTPD_ROOT /etc/apache2

# Apache HTTPD settings
ENV APACHE_SERVER_ROOT ${APP_HOME}/cfgov/apache
ENV APACHE_PROCESS_COUNT 4
ENV ACCESS_LOG /dev/stdout
ENV ERROR_LOG /dev/stderr
ENV STATIC_PATH ${APP_HOME}/cfgov/static/
ENV LIMIT_REQUEST_BODY 0

# mod_wsgi settings
ENV CFGOV_PATH ${APP_HOME}
ENV CFGOV_CURRENT ${APP_HOME}
ENV PYTHONPATH ${APP_HOME}/cfgov

# Django Settings
ENV DJANGO_SETTINGS_MODULE cfgov.settings.production
ENV DJANGO_STATIC_ROOT ${STATIC_PATH}
ENV ALLOWED_HOSTS '["*"]'

# Install Apache server and curl (container healthcheck),
# and converts all Docker Secrets into environment variables.
RUN apk add --no-cache apache2 curl && \
    echo '[ -d /var/run/secrets ] && cd /var/run/secrets && for s in *; do export $s=$(cat $s); done && cd -' > /etc/profile.d/secrets_env.sh

# Link mime.types for RHEL Compatability in apache config.
# TODO: Remove this link once RHEL is replaced
RUN ln -s /etc/apache2/mime.types /etc/mime.types

# Copy mod_wsgi.so from mod_wsgi image
COPY --from=cfgov-mod-wsgi /usr/lib/apache2/mod_wsgi.so /usr/lib/apache2/mod_wsgi.so

# Copy the cfgov directory form the build image
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/cfgov ${CFGOV_PATH}/cfgov
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/docker-entrypoint.sh ${CFGOV_PATH}/refresh-data.sh ${CFGOV_PATH}/initial-data.sh ${CFGOV_PATH}/
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/static.in ${CFGOV_PATH}/static.in

RUN ln -s /usr/lib/apache2 cfgov/apache/modules
RUN chown -R apache:apache ${APP_HOME} /usr/share/apache2 /var/run/apache2 /var/log/apache2

# Remove build dependencies for smaller image
RUN apk del .build-deps

USER apache

# Build frontend, cleanup excess file, and setup filesystem
# - cfgov/f/ - Wagtail file uploads
RUN rm -rf cfgov/apache/www cfgov/unprocessed && \
    mkdir -p cfgov/f

# Healthcheck retry set high since database loads take a while
HEALTHCHECK --start-period=300s --interval=30s --retries=30 \
            CMD curl -sf -A docker-healthcheck -o /dev/null http://localhost:8000

CMD ["httpd", "-d", "/src/consumerfinance.gov/cfgov/apache", "-f", "/src/consumerfinance.gov/cfgov/apache/conf/httpd.conf", "-D", "FOREGROUND"]
