FROM centos:7

# Set envvars required by apache
ENV CFGOV_PATH=/src/cfgov-refresh\
    STATIC_PATH=/src/cfgov-refresh/static/\
    APACHE_SERVER_ROOT=/src/cfgov-refresh/cfgov/apache\
    APACHE_WWW_PATH=/src/cfgov-refresh/cfgov/apache/www\
    CFGOV_SANDBOX=/src/cfgov-refresh/sandbox\
    APACHE_PROCESS_COUNT=4\
    ERROR_LOG=/proc/self/fd/1

# Install required packages
RUN yum install -y epel-release && \
    yum-config-manager --enable cr && \
    yum update -y && \
    yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y make gcc gcc-c++ kernel-devel mailcap which && \
    yum install -y postgresql10 postgresql10-devel && \
    yum install -y python-devel python36 python36-devel && \
    yum install -y httpd mod_wsgi && \
    yum clean all

# Copy over our requirement files to install
COPY requirements /src/requirements

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Copy over the script that enables fast serving of static files in prod
COPY docker/alias-static.sh /etc/profile.d/alias-static.sh

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

# Make the .env available in the bash shell
RUN echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc
