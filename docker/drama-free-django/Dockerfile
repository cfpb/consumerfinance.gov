FROM centos:6

ENV SCL_PYTHON_VERSION python27
ENV PIP_NO_CACHE_DIR true

ENV DFD_DIR /src/cfgov-refresh

# Must be world writable since alternate uid:gid may be patched in at `docker run` time.
RUN mkdir -p ${DFD_DIR} && chmod 777 ${DFD_DIR}
WORKDIR ${DFD_DIR}

# Install dependencies
RUN yum install -y centos-release-scl && \
    curl -sL https://rpm.nodesource.com/setup_10.x | bash - && \
    curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    yum install -y ${SCL_PYTHON_VERSION} gcc git nodejs which yarn && \
    echo "source scl_source enable ${SCL_PYTHON_VERSION}" > /etc/profile.d/scl_python.sh && \
    source /etc/profile && \
    pip install -U pip && \
    pip install -U git+https://github.com/cfpb/drama-free-django.git

COPY _build.sh _test.sh docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]