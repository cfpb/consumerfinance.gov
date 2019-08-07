FROM centos:7

# Install required packages
RUN yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y epel-release make gcc gcc-c++ kernel-devel mailcap which && \
    yum install -y postgresql10 postgresql10-devel && \
    yum install -y nmap-ncat python-devel python36 python36-devel && \
    yum clean all

# Copy over our requirement files to install
COPY requirements /src/requirements

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Make sure pip is installed
ADD https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
RUN python2.7 /src/get-pip.py 
RUN python3.6 -m ensurepip

# Make sure pip is up to date
RUN pip2.7 install -U pip
RUN pip3.6 install -U pip

# Install our requirements
RUN pip2.7 install -r /src/requirements/local.txt
RUN pip3.6 install -r /src/requirements/local.txt

# add wait-for-it.sh, https://github.com/vishnubob/wait-for-it
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Make the .env available in the bash shell
RUN echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc
