FROM centos:7 AS cfgov-dev

# Specify SCL-based Python version.
# Currently used options: python27, rh-python36
# See: https://www.softwarecollections.org/en/scls/user/rhscl/?search=python
ARG scl_python_version
ENV SCL_PYTHON_VERSION ${scl_python_version}

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

ENV APP_HOME /src/cfgov-refresh
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

SHELL ["/bin/bash", "--login", "-o", "pipefail", "-c"]

# Install common OS packages
RUN yum -y install \
        centos-release-scl \
        epel-release \
        https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    curl -sL https://rpm.nodesource.com/setup_10.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum -y install \
        mailcap \
        postgresql10 \
        which \
        ${SCL_PYTHON_VERSION} && \
    yum clean all && rm -rf /var/cache/yum && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > /etc/profile.d/enable_scl_python.sh && \
    source /etc/profile && \
    pip install --no-cache-dir --upgrade pip setuptools

# Disables pip cache. Reduces build time, and suppresses warnings when run as non-root.
# NOTE: MUST be after pip upgrade.  Build fails otherwise due to bug in old pip.
ENV PIP_NO_CACHE_DIR true

# Install python requirements
COPY requirements requirements

RUN yum -y install gcc && \
    pip install -r requirements/local.txt -r requirements/deployment.txt && \
    yum -y remove gcc && \
    yum clean all && rm -rf /var/cache/yum


EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "./cfgov/manage.py", "runserver", "0.0.0.0:8000"]



FROM cfgov-dev as cfgov-prod

ENV SCL_HTTPD_VERSION httpd24
ENV SCL_HTTPD_ROOT /opt/rh/${SCL_HTTPD_VERSION}/root

# Apache HTTPD settings
ENV APACHE_SERVER_ROOT ${SCL_HTTPD_ROOT}/etc/httpd
# FIXME: 
#ENV APACHE_SERVER_ROOT ${APP_HOME}/cfgov/apache
ENV APACHE_WWW_PATH ${SCL_HTTPD_ROOT}/var/www/html
ENV APACHE_PROCESS_COUNT 4
ENV ACCESS_LOG /dev/stdout
ENV ERROR_LOG /dev/stderr
ENV STATIC_PATH ${APACHE_WWW_PATH}/static
# FIXME: Figure out what to do this this!
ENV CFGOV_SANDBOX ???

# mod_wsgi settings
# FIXME: Can we get rid of this?  See wsgi.conf.
ENV CFGOV_PATH ${APP_HOME}
ENV CFGOV_CURRENT ${APP_HOME}
ENV PYTHONPATH ${APP_HOME}/cfgov

# Django Settings
ENV DJANGO_SETTINGS_MODULE cfgov.settings.production
ENV DJANGO_STATIC_ROOT ${STATIC_PATH}
ENV ALLOWED_HOSTS '["*"]'

RUN yum -y install ${SCL_HTTPD_VERSION} ${SCL_PYTHON_VERSION}-mod_wsgi && \
    yum clean all && rm -rf /var/cache/yum && \
    echo "source scl_source enable ${SCL_HTTPD_VERSION}" > /etc/profile.d/enable_scl_httpd.sh

# See .dockerignore for details on which files are included
COPY . .

# Build frontend
RUN yum -y install nodejs yarn  && \
    ./frontend.sh production && \
    cfgov/manage.py collectstatic && \
    yarn cache clean && \
    yum -y remove nodejs yarn && \
    yum clean all && rm -rf /var/cache/yum && \
    rm -rf \
        ${APACHE_SERVER_ROOT}/conf.d/* \
        ${APACHE_SERVER_ROOT}/conf.modules.d/* \
        cfgov/apache/conf.d/wsgi.conf \
        cfgov/apache/www \
        cfgov/unprocessed \
        node_modules && \
    mv cfgov/apache/conf.d/wsgi.conf.docker cfgov/apache/conf.d/wsgi.conf && \
    unalias cp && cp -R cfgov/apache/* ${APACHE_SERVER_ROOT}
# FIXME: If we go with a separate docker-compose.yml without the volumes, we could symlink httpd configs
#    ln -s ${SCL_HTTPD_ROOT}/etc/httpd/modules ${APACHE_SERVER_ROOT}/modules && \
#    ln -s ${SCL_HTTPD_ROOT}/etc/httpd/conf/magic ${APACHE_SERVER_ROOT}/conf/magic

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUND"]
#CMD ["httpd", "-d", "./cfgov/apache", "-D", "FOREGROUND"]

