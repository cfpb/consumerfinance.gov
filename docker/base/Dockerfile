FROM centos:6
#update this to force yum to update the package index
ENV UPDATED 20160816 

RUN yum -y update; yum clean all
RUN yum -y groupinstall 'Development Tools' && yum clean all
RUN yum -y install git centos-release-scl-rh ImageMagick-devel \
                   libxslt-devel libxml2-devel mysql-devel\
    && yum clean all
RUN yum -y install python27-python-devel && yum clean all
ADD enablepython27.sh /etc/profile.d/
RUN curl https://bootstrap.pypa.io/get-pip.py > /get-pip.py
RUN scl enable python27 "python /get-pip.py"

RUN curl  https://nodejs.org/download/release/v5.5.0/node-v5.5.0-linux-x64.tar.gz |  tar --strip-components 1  -xzv


