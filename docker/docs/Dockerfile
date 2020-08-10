FROM centos:7
RUN yum install -y which gcc gcc-c++ kernel-devel make epel-release && \
    yum install -y python36 && \
    yum clean all
COPY requirements /src/requirements
RUN python3.6 -m ensurepip
RUN pip3 install -U pip
RUN pip3 install -r /src/requirements/docs.txt
