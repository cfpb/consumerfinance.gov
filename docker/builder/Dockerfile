FROM centos:7

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

# Disables pip cache, which reduces build time, and suppresses warnings when
# run as non-root.
ENV PIP_NO_CACHE_DIR true

ENV BUILD_DIR /src/consumerfinance.gov

# Must be world writable since alternate uid:gid may be patched in at `docker
# run` time.
RUN mkdir -p ${BUILD_DIR} && chmod 777 ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

# Install all build requirements including Python 3 and the latest
# versions of the Python packages pip, setuptools, and wheel. Configure
# Python 3 to be enabled at login.
RUN yum -y update && \
    yum install -y centos-release-scl && \
    yum install -y rh-python38 gcc git && \
    source /etc/profile && \
    pip install --no-cache-dir -U pip setuptools wheel && \
    pip3 install --no-cache-dir -U pip setuptools wheel

COPY call_create.sh docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
