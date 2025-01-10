FROM centos:7 AS centos7-py38

COPY ./fix_centos_repos.sh .

RUN \
    ./fix_centos_repos.sh && \
    yum update -y && \
    yum install -y centos-release-scl && \
    ./fix_centos_repos.sh && \
    yum install -y rh-python38

FROM centos7-py38 AS cfgov-artifact-builder

RUN \
    yum install -y gcc && \
    source /opt/rh/rh-python38/enable && \
    pip install --no-cache-dir -U pip setuptools wheel

COPY ./build_cfgov_artifact.sh .

ENTRYPOINT ["./build_cfgov_artifact.sh"]

FROM centos7-py38 AS cfgov-artifact-tester

RUN yum install -y httpd24 rh-python38-mod_wsgi && \
    source /opt/rh/rh-python38/enable && \
    pip install --no-cache-dir virtualenv

COPY ./install_cfgov_and_run_apache.sh .

EXPOSE 80

HEALTHCHECK \
    --start-period=60s \
    CMD curl -f http://localhost/ || exit 1

ENTRYPOINT ["./install_cfgov_and_run_apache.sh"]
