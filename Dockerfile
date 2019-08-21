FROM centos:7 AS cfgov-base

SHELL ["/bin/bash", "--login", "-o", "pipefail", "-c"]

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

ENV APP_HOME /src/cfgov-refresh
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

# Install common OS packages
RUN yum -y install \
        centos-release-scl \
        epel-release \
        https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum -y install \
        mailcap \
	httpd \
        postgresql10 \
        which

# Specify SCL-based Python version.
# Currently used options: python27, rh-python36
# See: https://www.softwarecollections.org/en/scls/user/rhscl/?search=python
ARG scl_python_version
ENV SCL_PYTHON_VERSION ${scl_python_version}

# Install SCL-based Python, and set is as default `python`
RUN yum -y install ${SCL_PYTHON_VERSION} && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > \
         /etc/profile.d/enable_scl_python.sh && \
    source /etc/profile && \
    pip install --upgrade pip setuptools

EXPOSE 8000

COPY docker-entrypoint.sh ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]


# Image designed for local developement
FROM cfgov-base AS cfgov-develop

# Copy over our requirement files to install
COPY requirements requirements

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# add node and yarn repos
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo

# install dependencies with yum
RUN yum install -y nodejs yarn gcc httpd-devel postgresql10-devel && \
    yum clean all && rm -rf /var/cache/yum

# install python dependencies
RUN pip install --no-cache-dir -r requirements/local.txt
RUN pip install mod_wsgi

CMD ["python", "./cfgov/manage.py", "runserver", "0.0.0.0:8000"]

FROM cfgov-develop as cfgov-build

COPY cfgov/ ./cfgov
COPY config/ ./config
COPY gulp ./gulp
COPY static.in ./static.in
COPY scripts ./scripts

COPY frontend.sh gulpfile.js jest.config.js package.json yarn.lock /src/cfgov-refresh/

ENV DJANGO_SETTINGS_MODULE=cfgov.settings.production
ENV DJANGO_STATIC_ROOT=/var/www/html/static
ENV ALLOWED_HOSTS='["*"]'

RUN sh ./frontend.sh production

RUN cfgov/manage.py collectstatic

FROM cfgov-base as cfgov-deploy
ENV PY_LIB_DIR /opt/rh/${SCL_PYTHON_VERSION}/root/usr/lib/
ENV PY_LIB64_DIR /opt/rh/${SCL_PYTHON_VERSION}/root/usr/lib64/

COPY --from=cfgov-build ${PY_LIB_DIR} ${PY_LIB_DIR}
COPY --from=cfgov-build ${PY_LIB64_DIR} ${PY_LIB64_DIR}
COPY --from=cfgov-build --chown=apache:apache /src/cfgov-refresh/cfgov/ /src/cfgov-refresh/cfgov/
COPY --from=cfgov-build --chown=apache:apache /var/www/html/static /var/www/html/static
