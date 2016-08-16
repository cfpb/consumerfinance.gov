FROM centos:6
#update this to force yum to update the package index
ENV UPDATED 20160814 

RUN yum -y update; yum clean all
RUN yum -y install git && yum clean all
RUN yum -y groupinstall 'Development Tools' && yum clean all

WORKDIR /usr/local
RUN curl  https://nodejs.org/download/release/v5.5.0/node-v5.5.0-linux-x64.tar.gz |  tar --strip-components 1  -xzv
RUN npm install -g gulp bower
RUN echo '{ "allow_root":true}' > /root/.bowerrc

RUN mkdir /src
WORKDIR /src

ADD docker/frontend-runtime/entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

ENV TEST_HTTP_HOST django
ENV TEST_HTTP_PORT 8000

CMD entrypoint.sh
