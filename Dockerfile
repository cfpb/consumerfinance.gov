FROM centos:7

# Specify SCL-based Python version.
# Curretnly used options: python27, rh-python36
# See: https://www.softwarecollections.org/en/scls/user/rhscl/?search=python
ARG scl_python_version
ENV SCL_PYTHON_VERSION ${scl_python_version}

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

# FIXME: Do we want to support this when it only works in Python 3?
#        It won't hurt anything being here, but could result in different
#        experience in 2 vs. 3 when an hard error occurs.
ENV PYTHONFAULTHANDLER 1

# FIXME: Do we want to continue using this path?
#        There's a pseudo standard /usr/src/app used in many official images.
ENV APP_HOME /src/cfgov-refresh
WORKDIR ${APP_HOME}

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Overrides default `/bin/sh -c` shell, allowing use of /etc/profile.d
SHELL ["/bin/bash", "--login", "-c"]


# Install required packages
# Install common OS packages and enable SCL Python
RUN yum -y install \
        centos-release-scl \
        epel-release \
        https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum -y install \
        ${SCL_PYTHON_VERSION} \
        gcc \
        httpd \
        mailcap \
        postgresql10 \
        postgresql10-devel \
        which && \
    #echo "source scl_source enable ${SCL_PYTHON_VERSION}" | \
    #    tee --append /root/.bashrc /etc/profile.d/enable_scl_python.sh && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > \
         /etc/profile.d/enable_scl_python.sh && \
    #source /root/.bashrc && \
    source /etc/profile && \
    pip install --upgrade pip setuptools

# Copy over our requirement files to install
COPY requirements requirements

# Install our requirements
RUN pip install -r requirements/local.txt

EXPOSE 8000

# Uses "shell form" ENTRYPOINT so SHELL settings are not lost.
# SEE: https://docs.docker.com/engine/reference/builder/#shell-form-entrypoint-example
ENTRYPOINT ./docker-entrypoint.sh