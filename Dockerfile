FROM centos:7
RUN yum -y install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
RUN yum -y install which gcc gcc-c++ kernel-devel mailcap make mariadb mariadb-devel postgresql10 postgresql10-devel python-devel && yum clean all
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
run python /src/get-pip.py
copy requirements /src/requirements
run pip install -r /src/requirements/local.txt
copy extend-environment.sh /etc/profile.d/extend-environment.sh
