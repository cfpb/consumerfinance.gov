FROM centos:6

ENV SCL_PYTHON_VERSION python27

# Disables pip cache, which reduces build time, and suppresses warnings when run a non-root.
ENV PIP_NO_CACHE_DIR true

ENV DFD_DIR /src/cfgov-refresh

# Must be world writable since alternate uid:gid may be patched in at `docker run` time.
RUN mkdir -p ${DFD_DIR} && chmod 777 ${DFD_DIR}
WORKDIR ${DFD_DIR}

# Sets a consistent $HOME no matter which user the container runs under.  This prevents
# permissions issues caused by Docker's default `/` home directory.
ENV HOME /tmp/dfd-home
RUN mkdir -p ${HOME} && chmod 777 ${HOME}

# Install dependencies
# NOTE: You MUST upgrade pip before using it further.  The version packaged with SCL has issues
# with both setuptools and the PIP_NO_CACHE_DIR envvar (hence the --no-cache-dir override).
RUN yum install -y centos-release-scl && \
    curl -sL https://rpm.nodesource.com/setup_10.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum install -y ${SCL_PYTHON_VERSION} gcc git nodejs yarn && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > /etc/profile.d/scl_python.sh && \
    source /etc/profile && \
    pip install --no-cache-dir -U pip && \
    pip install -U git+https://github.com/cfpb/drama-free-django.git

COPY _build.sh _test.sh docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
