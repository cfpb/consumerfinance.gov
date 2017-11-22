FROM centos:7
RUN yum -y install which gcc gcc-c++ kernel-devel make mariadb mariadb-devel python-devel && yum clean all
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
run python /src/get-pip.py
copy requirements /src/requirements
run pip install -r /src/requirements/local.txt
copy extend-environment.sh /etc/profile.d/extend-environment.sh

# Search.gov API affiliate/access key
# ENV SEARCH_DOT_GOV_AFFILIATE=''
# ENV SEARCH_DOT_GOV_ACCESS_KEY=''
