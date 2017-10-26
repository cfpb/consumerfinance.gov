FROM python:2.7
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt
copy requirements /src/requirements
run pip install -r /src/requirements/local.txt
