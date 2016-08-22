FROM cfgov_base

ENV PYTHONPATH /src/cfgov
ENV DJANGO_SETTINGS_MODULE cfgov.settings.local

ADD requirements/ /python-requirements
RUN scl enable python27 "pip install -r /python-requirements/local.txt"
RUN scl enable python27 "pip install -r /python-requirements/test.txt"

ADD docker/django/entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

CMD entrypoint.sh
WORKDIR /src
