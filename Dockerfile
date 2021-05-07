FROM centos:7 AS cfgov-dev

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

LABEL maintainer="tech@cfpb.gov"

# Specify SCL-based Python version
# Currently used option: rh-python36
# See: https://www.softwarecollections.org/en/scls/user/rhscl/?search=python
ARG scl_python_version
ENV SCL_PYTHON_VERSION ${scl_python_version}
ARG postgres_version
ENV POSTGRES_VERSION ${postgres_version}

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

ENV APP_HOME /src/consumerfinance.gov
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

SHELL ["/bin/bash", "--login", "-o", "pipefail", "-c"]

# Install common OS packages
RUN yum -y install \
        centos-release-scl \
        epel-release && \
    yum -y install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    curl -sL https://rpm.nodesource.com/setup_14.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum -y update && \
    yum -y install \
        gcc \
        git \
        mailcap \
        ${POSTGRES_VERSION} \
        which \
        gettext \
        ${SCL_PYTHON_VERSION} && \
    yum clean all && rm -rf /var/cache/yum && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > /etc/profile.d/enable_scl_python.sh && \
    source /etc/profile && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

# Disables pip cache. Reduces build time, and suppresses warnings when run as non-root.
# NOTE: MUST be after pip upgrade. Build fails otherwise due to bug in old pip.
ENV PIP_NO_CACHE_DIR true

# Install python requirements
COPY requirements requirements
RUN pip install -r requirements/local.txt -r requirements/deployment.txt

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

# Install Node.js version curled earlier in this file from rpm.nodesource.com
RUN yum -y install nodejs yarn && \
    ./frontend.sh production && \
    cfgov/manage.py collectstatic && \
    yarn cache clean && \
    rm -rf node_modules npm-packages-offline-cache


# Production-like Apache-based image
FROM cfgov-dev as cfgov-prod

ENV SCL_HTTPD_VERSION httpd24
ENV SCL_HTTPD_ROOT /opt/rh/${SCL_HTTPD_VERSION}/root

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

# Install and enable SCL-based Apache server and mod_wsgi,
# and converts all Docker Secrets into environment variables.
RUN yum -y install ${SCL_HTTPD_VERSION} ${SCL_PYTHON_VERSION}-mod_wsgi && \
    yum clean all && rm -rf /var/cache/yum && \
    echo "source scl_source enable ${SCL_HTTPD_VERSION}" > /etc/profile.d/enable_scl_httpd.sh && \
    echo '[ -d /var/run/secrets ] && cd /var/run/secrets && for s in *; do export $s=$(cat $s); done && cd -' > /etc/profile.d/secrets_env.sh

# Copy the cfgov directory form the build image
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/cfgov ${CFGOV_PATH}/cfgov
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/docker-entrypoint.sh ${CFGOV_PATH}/refresh-data.sh ${CFGOV_PATH}/
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/static.in ${CFGOV_PATH}/static.in


RUN yum clean all && rm -rf /var/cache/yum && \
    chown -R apache:apache ${APP_HOME} ${SCL_HTTPD_ROOT}/usr/share/httpd ${SCL_HTTPD_ROOT}/var/run

ENV PATH="/opt/rh/${SCL_PYTHON_VERSION}/root/usr/bin:${PATH}"

# Remove files flagged by image vulnerability scanner
RUN cd /opt/rh/rh-python36/root/usr/lib/python3.6/site-packages/ && \
    rm -f ndg/httpsclient/test/pki/localhost.key sslserver/certs/development.key

USER apache

# Build frontend, cleanup excess file, and setup filesystem
# - cfgov/f/ - Wagtail file uploads
RUN ln -s ${SCL_HTTPD_ROOT}/etc/httpd/modules ${APACHE_SERVER_ROOT}/modules && \
    ln -s ${SCL_HTTPD_ROOT}/etc/httpd/run ${APACHE_SERVER_ROOT}/run && \
    rm -rf cfgov/apache/www cfgov/unprocessed && \
    mkdir -p cfgov/f

# Healthcheck retry set high since database loads take a while
HEALTHCHECK --start-period=300s --interval=30s --retries=30 \
            CMD curl -sf -A docker-healthcheck -o /dev/null http://localhost:8000

CMD ["httpd", "-d", "cfgov/apache", "-D", "FOREGROUND"]
