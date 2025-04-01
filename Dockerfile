FROM python:3.8-alpine as python

# Hard labels
LABEL maintainer="tech@cfpb.gov"

# Create a non-root user
ARG USERNAME=cfgov
ARG USER_UID=1000
RUN addgroup --gid ${USER_UID} ${USERNAME} && \
    adduser \
        --uid ${USER_UID} \
        --ingroup ${USERNAME} \
        --disabled-password \
        ${USERNAME}

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8

# Disable pip cache dir
ENV PIP_NO_CACHE_DIR 1

# Allow pip install as root.
ENV PIP_ROOT_USER_ACTION ignore

# Stops Python default buffering to stdout, improving logging to the console
ENV PYTHONUNBUFFERED 1

# Set the APP_HOME, our working directory
ENV APP_HOME /src/consumerfinance.gov

# Add our top-level Python path to the PYTHONPATH
ENV PYTHONPATH ${APP_HOME}/cfgov

# Set the working directory
WORKDIR ${APP_HOME}

# Copy the application requirements, needed to build the Python environment
# below
# Note: by specifying specific files we enable this layer to be cached if
# these files do not change.
COPY requirements ./requirements

# Build the Python environment
RUN \
    apk update --no-cache && apk upgrade --no-cache && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        gettext \
        git \
        libffi-dev \
        musl-dev \
        postgresql-dev \
    && \
    apk add --no-cache --virtual .backend-deps \
        bash \
        curl \
        postgresql \
    && \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements/deployment_container.txt && \
    apk del .build-deps

# The application will run on port 8000
EXPOSE 8000

#######################################################################
# Build frontend assets using a Node base image
FROM node:20-alpine as node-builder

ENV APP_HOME /src/consumerfinance.gov
WORKDIR ${APP_HOME}

# Install and update common OS packages and frontend dependencies
RUN apk update --no-cache && apk upgrade --no-cache && \
    apk add --no-cache --virtual .frontend-deps \
        jpeg-dev \
        yarn \
        zlib-dev

# Target a production frontend build
ARG FRONTEND_TARGET=production

# Copy the files needed for building the frontend
# Note: by specifying specific files we enable this layer to be cached if
# these files do not change.
COPY frontend.sh .
COPY package.json .
COPY yarn.lock .
COPY cfgov/unprocessed ./cfgov/unprocessed
COPY config  ./config/
COPY esbuild  ./esbuild/
COPY scripts ./scripts/
COPY npm-packages-offline-cache ./npm-packages-offline-cache/

# Build the front-end
RUN ./frontend.sh  ${FRONTEND_TARGET} && \
    yarn cache clean && \
    rm -rf \
        frontend.sh \
        package.json \
        yarn.lock \
        cfgov/unprocessed \
        config \
        esbuild \
        scripts \
        npm-packages-offline-cache \
        node_modules

#######################################################################
# Dev runs with Django runserver with cfgov.settings.local
FROM python AS dev

# Django Settings
ENV DJANGO_SETTINGS_MODULE cfgov.settings.local
ENV ALLOWED_HOSTS '["*"]'

# Install dev/local Python requirements
RUN pip install -r requirements/local.txt

# Copy the necessary files and directories into the dev container
# Note: by specifying specific files we enable this layer to be cached if
# these files do not change.
COPY cfgov ./cfgov/
COPY static.in ./static.in/
COPY docker-entrypoint.sh ./docker-entrypoint.sh
COPY --from=node-builder ${APP_HOME} ${APP_HOME}

# Run our initial data entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]

# Give our user ownership over the app directory
RUN chown -R ${USERNAME}:${USERNAME} ${APP_HOME}

# Run the application with the user we created
USER $USERNAME

# Run Django's runserver
CMD python ./cfgov/manage.py runserver 0.0.0.0:8000

#######################################################################
# Production runs with Django via Gunicorn with cfgov.settings.production
FROM python AS prod

# Django Settings
ENV DJANGO_SETTINGS_MODULE cfgov.settings.production
ENV STATIC_PATH ${APP_HOME}/cfgov/static/
ENV DJANGO_STATIC_ROOT ${STATIC_PATH}
ENV ALLOWED_HOSTS '["*"]'

# Copy the application code over
COPY cfgov ./cfgov/
COPY static.in ./static.in/
COPY refresh-data.sh .
COPY initial-data.sh .
COPY index.sh .
COPY test.sql.gz .

# Copy our static build over from node-builder
COPY --from=node-builder ${APP_HOME} ${APP_HOME}

# Run Django's collectstatic to collect assets from the frontend build.
#
# Our Django settings file requires a SECRET_KEY, but we don't want to
# bake our key into the Docker image. We need to provide one in order to
# be able to run collectstatic, even though the key value isn't actually
# used in any way during staticfiles collection. We provide a random
# secret key here for this step only.
RUN SECRET_KEY=only-for-collectstatic cfgov/manage.py collectstatic --noinput

# Give our user ownership over the app directory
RUN chown -R ${USERNAME}:${USERNAME} ${APP_HOME}

# Run the application with the user we created
USER $USERNAME

# Run Gunicorn
CMD gunicorn --reload cfgov.wsgi:application -b :8000
