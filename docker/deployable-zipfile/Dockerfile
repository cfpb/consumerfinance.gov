FROM centos:7

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

#for a positive test of the github action
ENV test true

# Disables pip cache, which reduces build time, and suppresses warnings when
# run as non-root.
ENV PIP_NO_CACHE_DIR true

ENV BUILD_DIR /src/consumerfinance.gov

# Must be world writable since alternate uid:gid may be patched in at `docker
# run` time.
RUN mkdir -p ${BUILD_DIR} && chmod 777 ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

# Sets a consistent $HOME no matter which user the container runs under. This
# prevents permissions issues caused by Docker's default `/` home directory.
ENV HOME /tmp/dfd-home
RUN mkdir -p ${HOME} && chmod 777 ${HOME}

# Install all build requirements including Python 3 and the latest
# versions of the Python packages pip, setuptools, and wheel. Configure
# Python 3 to be enabled at login.
RUN yum -y update && \
    yum install -y centos-release-scl && \
    rpm -i https://rpm.nodesource.com/pub_16.x/el/7/x86_64/nodejs-16.13.1-1nodesource.x86_64.rpm && \
    curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum install -y rh-python38 gcc git nodejs yarn && \
    echo "source scl_source enable rh-python38" > /etc/profile.d/scl_python.sh && \
    source /etc/profile && \
    pip install --no-cache-dir -U pip setuptools wheel && \
    pip3 install --no-cache-dir -U pip setuptools wheel

COPY _build.sh docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
