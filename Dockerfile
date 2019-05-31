FROM centos:7 as runtime

# Install build-required packages
RUN yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y epel-release mailcap which httpd && \
    yum install -y postgresql10  && \
    yum install -y python36 && \
    yum clean all


FROM runtime AS dev

# Install build-required packages
RUN curl -sL https://rpm.nodesource.com/setup_8.x | bash -
RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo

RUN yum install -y nodejs yarn make gcc gcc-c++ kernel-devel unzip && \
    yum install -y httpd-devel postgresql10-devel && \
    yum install -y python-devel python-pip python36-devel && \
    yum clean all
RUN npm install -g gulp

# Copy over our requirement files to install
COPY requirements /src/requirements

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Make sure pip is installed
RUN pip2 install -U pip
RUN python3.6 -m ensurepip

# Make sure pip is up to date
RUN pip2.7 install -U pip setuptools mod_wsgi pytz
RUN pip3.6 install -U pip mod_wsgi pytz

# Install our python requirements
RUN pip2.7 install -r /src/requirements/local.txt
RUN pip3.6 install -r /src/requirements/local.txt

# Make the .env available in the bash shell
RUN echo 'source /src/cfgov-refresh/.env' >> ~/.bashrc

FROM dev as gulp
RUN mkdir /src/cfgov-refresh
WORKDIR /src/cfgov-refresh

COPY scripts scripts
COPY frontend.sh .
COPY package.json .
COPY code.json .
COPY yarn.lock .
COPY babel.config.js .
COPY gulpfile.js .
COPY gulp gulp
COPY config config
COPY jest.config.js .
COPY cfgov/ ./cfgov/
COPY cfgov-fonts-master.zip /tmp/fonts.zip

ENV DJANGO_SETTINGS_MODULE=cfgov.settings.minimal_collectstatic
ENV ALLOWED_HOSTS='["*"]'
RUN sh frontend.sh production
RUN mkdir static.in
RUN unzip /tmp/fonts.zip -d ./static.in/
RUN cfgov/manage.py collectstatic


FROM runtime as deployment
ENV DJANGO_SETTINGS_MODULE=cfgov.settings.production
ENV ALLOWED_HOSTS='["*"]'
ENV PYTHONPATH=/srv/cfgov/current/cfgov/
COPY --from=gulp /usr/lib64/python2.7/site-packages/ /usr/lib64/python2.7/site-packages/
COPY --from=gulp /usr/lib/python2.7/site-packages/ /usr/lib/python2.7/site-packages/
COPY --from=gulp /usr/local/lib64/python3.6/site-packages/ /usr/local/lib64/python3.6/site-packages/
COPY --from=gulp /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY --from=gulp /src/cfgov-refresh/ /src/cfgov-refresh/
COPY /src/cfgov-refresh/docker/ /src/cfgov-refresh/docker/
WORKDIR /src/cfgov-refresh
RUN chown -R apache:apache .
USER apache:apache
CMD cfgov/manage.py runmodwsgi 
