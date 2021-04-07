FROM cypress/base:centos7-12.4.0

LABEL maintainer="tech@cfpb.gov"

ENV CYPRESS_VERSION 7.0.1

RUN mkdir -p /app
WORKDIR /app

# Update and install OS dependencies
RUN yum update -y && \
    yum -y install wget && \
    yum clean all && rm -rf /var/cache/yum

# Install Chrome browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum -y install google-chrome-stable_current_x86_64.rpm ; \
    rm -f ./google-chrome-stable_current_x86_64.rpm
RUN google-chrome --version

# Install Cypress
RUN npm install -D cypress && \
    $(npm bin)/cypress verify

# Remove files flagged by image vulnerability scanner
RUN cd /root/.cache/Cypress/${CYPRESS_VERSION}/Cypress/resources/app/packages/server/node_modules/ && \
    rm -rf http-proxy/test/fixtures/agent2-key.pem lazystream/secret && \
    rm -rf public-encrypt/test/*.pem public-encrypt/test/*.priv
RUN cd /usr/lib64/python2.7/site-packages/bzrlib/tests/ssl_certs/ && \
    rm -f server_with_pass.key server_without_pass.key && \
    rm -f /etc/pki/tls/private/localhost.key

# Set User to Non Root
RUN adduser -s /bin/false cypress && \
    mv /root/.cache /home/cypress/.cache && \
    chown -R cypress:cypress ./ /home/cypress/.cache

ENV CYPRESS_CACHE_FOLDER /home/cypress/.cache/Cypress

USER cypress
