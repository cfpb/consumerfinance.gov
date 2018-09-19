FROM centos:7
RUN yum -y install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum -y install which gcc gcc-c++ git kernel-devel mailcap make postgresql10 postgresql10-devel python-devel && \
    curl --silent --location https://rpm.nodesource.com/setup_10.x | bash - && \
    yum -y install nodejs && \
    yum clean all
WORKDIR /src
ADD . /src
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
RUN python /src/get-pip.py && \
  npm set unsafe-perm true && \
  /src/setup.sh docker
