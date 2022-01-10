FROM centos:7

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

# Install all build requirements including Python 3.9 and the latest
# versions of the Python packages pip, setuptools, and wheel. Configure
# Python 3.9 to be enabled at login.

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

ENV BUILD_DIR /src/consumerfinance.gov

# Must be world writable since alternate uid:gid may be patched in at `docker
# run` time.
RUN mkdir -p ${BUILD_DIR} && chmod 777 ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

# Sets a consistent $HOME no matter which user the container runs under. This
# prevents permissions issues caused by Docker's default `/` home directory.
ENV HOME /tmp/dfd-home
RUN mkdir -p ${HOME} && chmod 777 ${HOME}
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
# Disables pip cache. Reduces build time, and suppresses warnings when run as non-root.
# NOTE: MUST be after pip upgrade. Build fails otherwise due to bug in old pip.
ENV PIP_NO_CACHE_DIR true

RUN yum -y update && \
    yum install -y centos-release-scl && \
    rpm -i https://rpm.nodesource.com/pub_16.x/el/7/x86_64/nodejs-16.13.1-1nodesource.x86_64.rpm && \
    curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo

COPY _build.sh docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
