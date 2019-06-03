FROM centos:7 as cfgov-runtime

# Install build-required packages
RUN yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y epel-release mailcap which httpd && \
    yum install -y postgresql10  && \
    yum install -y python36 && \
    yum clean all

RUN mkdir -p /var/log/httpd
RUN chown -R apache:apache /var/log/httpd

ENV PYTHON /usr/bin/python3
ENV PYTHONPATH=/src/cfgov-refresh/cfgov/
COPY docker/python/entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]
CMD ["sh", "-c", "/usr/local/bin/python /src/cfgov-refresh/cfgov/manage.py runmodwsgi --port 8000 --user apache --group apache --log-to-terminal --working-directory /src/cfgov-refresh/  $EXTRA_MODWSGI_ARGS"]


FROM cfgov-runtime AS cfgov-dev

# Install build-required packages
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
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
COPY cfgov-fonts-master.zip /tmp/fonts.zip

ENV DJANGO_SETTINGS_MODULE=cfgov.settings.minimal_collectstatic
ENV ALLOWED_HOSTS='["*"]'

# install optional apps
RUN pip2 install -r /src/requirements/optional-public.txt

# Commented out because retirement wheel is not Python3 compatible yet
# RUN pip3.6 install -r /src/requirements/optional-public.txt

RUN sh frontend.sh production
RUN mkdir static.in
RUN unzip /tmp/fonts.zip -d ./static.in/
RUN cfgov/manage.py collectstatic


FROM cfgov-runtime as cfgov-deployment
ENV DJANGO_SETTINGS_MODULE=cfgov.settings.production
ENV ALLOWED_HOSTS='["*"]'
COPY --from=cfgov-build /usr/lib64/python2.7/site-packages/ /usr/lib64/python2.7/site-packages/
COPY --from=cfgov-build /usr/lib/python2.7/site-packages/ /usr/lib/python2.7/site-packages/
COPY --from=cfgov-build /usr/local/lib64/python3.6/site-packages/ /usr/local/lib64/python3.6/site-packages/
COPY --from=cfgov-build /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY --from=cfgov-build /src/cfgov-refresh/cfgov/ /src/cfgov-refresh/cfgov/
COPY --from=cfgov-build /var/www/html/static /var/www/html/static
WORKDIR /src/cfgov-refresh
RUN chown -R apache:apache .
EXPOSE 8000
