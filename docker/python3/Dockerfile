FROM centos:7
RUN yum -y install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum -y install which gcc gcc-c++ kernel-devel mailcap make postgresql10 postgresql10-devel python-devel && \
    yum install -y python36 && \
    yum clean all
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
COPY requirements /src/requirements
COPY extend-environment.sh /etc/profile.d/extend-environment.sh
RUN python3.6 -m ensurepip
RUN pip3 install -U pip
RUN pip3 install -r /src/requirements/local.txt
RUN echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc
