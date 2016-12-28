FROM cfgov/base

ENV PYTHONPATH /src/cfgov
ENV DJANGO_SETTINGS_MODULE cfgov.settings.local
ENV MYSQL_HOST mysql
ENV MYSQL_NAME v1
ENV MEDIA_ROOT /var/media

ADD requirements/ /python-requirements
RUN scl enable python27 "pip install -r /python-requirements/local.txt" && \
    scl enable python27 "pip install -r /python-requirements/test.txt" && \
    rm -rf /root/.cache/pip/

ADD docker/django/entrypoint.sh /usr/local/bin
ADD docker/django/develop-apps.sh /etc/profile.d/develop-apps.sh
RUN mkdir /var/media
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chmod +x /etc/profile.d/develop-apps.sh

ENTRYPOINT ["scl","enable", "python27", "--"]
CMD entrypoint.sh
VOLUME /var/media
WORKDIR /src
EXPOSE 8000
