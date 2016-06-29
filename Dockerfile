FROM vickumar/python-nodejs

ENV PYTHONUNBUFFERED 1

ENV MYSQL_NAME "v1"
ENV MYSQL_USER "v1"
ENV MYSQL_PW "password"
ENV MYSQL_HOST "mysql"
ENV ES_HOST "search"

ENV STAGING_HOSTNAME "content.localhost"
ENV DJANGO_STATIC_ROOT "/code/cfgov-refresh/cfgov/static_built"
ENV WAGTAIL_ADMIN_PW "admin"
ENV ADMIN_EMAILS "emmanuel.apau@excella.com;kaveiii@gmail.com"
ENV EMAIL_SUBJECT_PREFIX "[CFPB]: "
ENV WAGTAILADMIN_NOTIFICATION_FROM_EMAIL "cfpb@github.io"
ENV LOGIN_FAIL_TIME_PERIOD "5"
ENV LOGIN_FAILS_ALLOWED "20"
ENV INITIAL_DATA_PATH "/code/cfgov-refresh/cfgov/v1/util/initial-data.py"
ENV SHEER_ELASTICSEARCH_INDEX "content"
ENV VIRTUAL_ENV "v1"
ENV OAH_SHEER_PATH "/code/cfgov-refreshapps/owning-a-home/dist"
ENV TAX_TIME_SHEER_PATH "/code/cfgov-refreshapps/tax-time-saving/dist"
ENV KBYO_SHEER_PATH "apps/know-before-you-owe/dist"

ENV PYTHONPATH "$PYTHONPATH:/code/apps/agreement_database:/code/apps/ccdb-content:/code/apps/college-costs:/code/apps/django-college-cost-comparison:/code/apps/django-hud:/code/apps/eregs:/code/apps/knowledgebase:/code/apps/leadership-calendar:/code/apps/owning-a-home-api:/code/apps/picard:/code/apps/regulations-core:/code/apps/regulations-site:/code/apps/retirement:/code/apps/selfregistration"

RUN mkdir -p /code
RUN mkdir -p /collectstatic
WORKDIR /code
ADD . /code
EXPOSE 8000
