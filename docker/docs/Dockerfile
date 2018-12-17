FROM centos:7
RUN yum install -y which gcc gcc-c++ kernel-devel make epel-release && \
    yum install -y python36 && \
    yum clean all
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
COPY requirements /src/requirements
RUN python3.6 /src/get-pip.py && pip install -r /src/requirements/docs.txt
