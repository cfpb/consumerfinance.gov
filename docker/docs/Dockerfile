FROM python:3-alpine

# Hard labels
LABEL maintainer="tech@cfpb.gov"

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
ENV ENV /etc/profile
ENV PIP_NO_CACHE_DIR true
# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

COPY requirements/docs.txt /src/requirements.txt
RUN pip install -U pip -r /src/requirements.txt
