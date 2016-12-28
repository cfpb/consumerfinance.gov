FROM cfgov/base
#update this to force yum to update the package index

RUN npm install -g gulp bower
RUN echo '{ "allow_root":true}' > /root/.bowerrc

RUN mkdir /src
WORKDIR /src
ADD package.json ./
RUN npm install && mv node_modules ../
ADD docker/gulp/entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

ENV TEST_HTTP_HOST django
ENV TEST_HTTP_PORT 8000

EXPOSE 3000
CMD entrypoint.sh
