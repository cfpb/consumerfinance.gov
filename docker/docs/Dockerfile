FROM python:3.9-alpine
#for a positive test of the github action
ENV test true

COPY requirements /src/requirements
RUN pip install -U pip
RUN pip install -r /src/requirements/docs.txt
