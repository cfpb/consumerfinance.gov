FROM centos:6
#update this to force yum to update the package index
ENV UPDATED 20160814 
ENV PYTHONPATH /src/cfgov

RUN yum -y update; yum clean all
RUN yum -y install git centos-release-scl-rh && yum clean all
RUN yum -y groupinstall 'Development Tools' && yum clean all
RUN yum -y install python27-python-devel ImageMagick-devel\
                    libxslt-devel libxml2-devel mysql-devel

RUN curl https://bootstrap.pypa.io/get-pip.py > /get-pip.py
RUN scl enable python27 "python /get-pip.py"

WORKDIR /usr/local
RUN curl  https://nodejs.org/download/release/v5.5.0/node-v5.5.0-linux-x64.tar.gz |  tar --strip-components 1  -xzv

RUN mkdir /python-requirements
ADD requirements/ /python-requirements
RUN scl enable python27 "pip install -r /python-requirements/local.txt"
RUN scl enable python27 "pip install -r /python-requirements/test.txt"

ADD docker/backend-runtime/entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /src
