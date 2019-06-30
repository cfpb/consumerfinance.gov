FROM centos:7 as cfgov-runtime

# Install build-required packages
RUN yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y epel-release mailcap which httpd && \
    yum install -y postgresql10  && \
    yum install -y python36 && \
    yum clean all && rm -rf /var/cache/yum

ENV PYTHON /usr/bin/python36
ENV PYTHONPATH=/src/cfgov-refresh/cfgov/
RUN echo "export PATH=/active-python:$PATH" > /etc/profile.d/active-python.sh
COPY docker/python/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN mkdir /active-python/ && chown -R apache:apache /active-python

ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]
CMD ["sh", "-c", "/active-python/python /src/cfgov-refresh/cfgov/manage.py runmodwsgi --port 8000 --user apache --group apache\
                                                                                      --log-to-terminal\
                                                                                      --working-directory /src/cfgov-refresh/\
                                                                                      --include-file /src/cfgov-refresh/cfgov/apache/include.conf\
                                                                                       $EXTRA_MODWSGI_ARGS"]
EXPOSE 8000


FROM cfgov-runtime AS cfgov-dev

# Install build-required packages
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo

RUN yum install -y nodejs yarn make gcc gcc-c++ kernel-devel unzip && \
    yum install -y httpd-devel postgresql10-devel && \
    yum install -y python-devel python-pip python36-devel && \
    yum clean all && rm -rf /var/cache/yum

# Copy over our requirement files to install
COPY requirements /src/requirements

# Copy over the script that extends the Python environment with develop-apps
COPY extend-environment.sh /etc/profile.d/extend-environment.sh

# Make sure pip and setuptools current
RUN pip2 install -U pip setuptools
RUN python3.6 -m ensurepip
RUN pip3.6 install -U pip setuptools

# Install our python requirements
RUN pip2.7 install -r /src/requirements/local.txt
RUN pip3.6 install -r /src/requirements/local.txt

ENV EXTRA_MODWSGI_ARGS "--reload-on-changes"

FROM cfgov-dev as cfgov-build
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

RUN sh frontend.sh production

COPY requirements/ ./requirements/
COPY cfgov-fonts-master.zip .
RUN mkdir static.in && unzip cfgov-fonts-master.zip -d ./static.in/
COPY build-artifact.sh .
RUN ./build-artifact.sh docker

FROM cfgov-runtime as cfgov-deployment
ENV DJANGO_SETTINGS_MODULE=cfgov.settings.production
ENV ALLOWED_HOSTS='["*"]'
COPY --from=cfgov-build /src/cfgov-refresh/build/docker.tgz /tmp/docker.tgz
WORKDIR /
RUN tar -zxvf /tmp/docker.tgz
RUN which python
RUN /srv/cfgov/docker/activate.sh
USER apache
CMD ["/etc/cfgov-apache/apachectl", "-D", "FOREGROUND"]
