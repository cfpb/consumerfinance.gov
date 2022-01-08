FROM centos:7 AS cfgov-dev

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

LABEL maintainer="tech@cfpb.gov"


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
    rpm -i https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum -y update && \
    yum -y install \
        gcc \
        git \
        mailcap \
        postgresql10 \
        which \
        gettext && \
    yum clean all && rm -rf /var/cache/yum

# Build python
WORKDIR /tmp
ENV PYTHONVERSION=3.9.9
ENV PYTHON_ARCHIVE_MD5HASH=a2da2a456c078db131734ff62de10ed5
RUN yum install -y epel-release
RUN yum groupinstall -y "Development Tools"
RUN yum install -y bzip2-devel libffi-devel openssl-devel readline-devel sqlite-devel tk-devel wget xz-devel zlib-devel
RUN gcc --version
RUN wget https://www.python.org/ftp/python/${PYTHONVERSION}/Python-${PYTHONVERSION}.tgz
RUN echo "${PYTHON_ARCHIVE_MD5HASH} Python-${PYTHONVERSION}.tgz" | md5sum -c
RUN tar xvf Python-${PYTHONVERSION}.tgz
RUN cd Python-${PYTHONVERSION}/ && \
    ./configure --enable-shared --enable-optimiztions --with-ensurepip=install --prefix=/usr/local LDFLAGS="-Wl,-rpath /usr/local/lib" && \
    make altinstall && make bininstall
RUN rm -Rf Python* *.pem
RUN yum remove -y bzip2-devel libffi-devel openssl-devel readline-devel sqlite-devel tk-devel wget xz-devel zlib-devel
RUN yum groupremove -y "Development Tools"
RUN yum remove -y epel-release
RUN yum clean all
WORKDIR ${APP_HOME}

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Disables pip cache. Reduces build time, and suppresses warnings when run as non-root.
# NOTE: MUST be after pip upgrade. Build fails otherwise due to bug in old pip.
ENV PIP_NO_CACHE_DIR true

# Install python requirements
RUN yum install -y postgresql-devel
RUN yum install -y python3-devel.x86_64
COPY requirements requirements
RUN echo requirements/local.txt
RUN python3 -m pip install -r requirements/local.txt -r requirements/deployment.txt

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "./cfgov/manage.py", "runserver", "0.0.0.0:8000"]

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
RUN yum -y install ${SCL_HTTPD_VERSION} && \
    yum clean all && rm -rf /var/cache/yum && \
    echo "source scl_source enable ${SCL_HTTPD_VERSION}" > /etc/profile.d/enable_scl_httpd.sh && \
    echo '[ -d /var/run/secrets ] && cd /var/run/secrets && for s in *; do export $s=$(cat $s); done && cd -' > /etc/profile.d/secrets_env.sh

# Copy the cfgov directory form the build image
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/cfgov ${CFGOV_PATH}/cfgov
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/docker-entrypoint.sh ${CFGOV_PATH}/refresh-data.sh ${CFGOV_PATH}/
COPY --from=cfgov-build --chown=apache:apache ${CFGOV_PATH}/static.in ${CFGOV_PATH}/static.in

# Build mod_wsgi
WORKDIR /tmp
RUN yum groupinstall -y "Development Tools"
RUN yum install -y ${SCL_HTTPD_VERSION}-httpd-devel wget
RUN wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.0.tar.gz -O mod_wsgi.tar.gz
RUN tar xzvf mod_wsgi.tar.gz
RUN mv mod_wsgi-* mod_wsgi
RUN cd mod_wsgi && ./configure --with-python=/usr/local/bin/python3 && make && make install
RUN rm -Rf mod_wsgi*
RUN yum groupremove -y "Development Tools"
RUN yum remove -y ${SCL_HTTPD_VERSION}-httpd-devel wget
WORKDIR ${APP_HOME}

# Clean up
RUN yum clean all && rm -rf /var/cache/yum && \
    chown -R apache:apache ${APP_HOME} ${SCL_HTTPD_ROOT}/usr/share/httpd ${SCL_HTTPD_ROOT}/var/run

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
