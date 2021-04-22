FROM centos:7

LABEL maintainer="tech@cfpb.gov"

RUN mkdir -p /app
WORKDIR /app

# avoid too many progress messages
# https://github.com/cypress-io/cypress/issues/1243
ENV CI=1

# Update and install Cypress dependencies, Node.js, and Chrome browser
# https://docs.cypress.io/guides/continuous-integration/introduction#Dependencies
RUN yum update -y && \
    yum -y install gcc-c++ make wget && \
    curl -sL https://rpm.nodesource.com/setup_current.x | bash - && \
    yum install -y nodejs && \
    npm install yarn -g && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum -y install google-chrome-stable_current_x86_64.rpm ; \
    rm -f ./google-chrome-stable_current_x86_64.rpm ; \
    google-chrome --version && \
    yum -y install \
        xorg-x11-server-Xvfb \
        xorg-x11-xauth \
        gtk3-3.22* \
        libXtst* \
        libXScrnSaver* \
        GConf2* \
        nss* \
        alsa-lib* && \
    yum clean all && rm -rf /var/cache/yum && \
    npm install -D cypress && \
    $(npm bin)/cypress verify

# Remove files flagged by image vulnerability scanner
RUN cd /root/.cache/Cypress/*/Cypress/resources/app/packages/server/node_modules/ && \
    rm -rf http-proxy/test/fixtures/agent2-key.pem lazystream/secret && \
    rm -f public-encrypt/test/*.pem public-encrypt/test/*.priv && \
    rm -f /etc/pki/tls/private/localhost.key

# Set User to Non Root
RUN adduser -s /bin/false cypress && \
    mv /root/.cache /home/cypress/.cache && \
    chown -R cypress:cypress ./ /home/cypress/.cache

ENV CYPRESS_CACHE_FOLDER /home/cypress/.cache/Cypress

USER cypress
