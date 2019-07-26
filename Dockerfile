# Base image inherited by all cfgov-refresh child images
FROM centos:7 AS cfgov-base

SHELL ["/bin/bash", "--login", "-c"]

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
        gcc \
        httpd \
        mailcap \
        postgresql10 \
        postgresql10-devel \
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

# Copy over our requirement files to install
COPY requirements requirements

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]


# Image designed for local developement
FROM cfgov-base AS cfgov-develop

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Install our requirements
RUN pip install --no-cache-dir -r requirements/local.txt

CMD ["python", "./cfgov/manage.py", "runserver", "0.0.0.0:8000"]
