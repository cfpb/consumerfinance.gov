FROM cypress/base:centos7-12.4.0

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

# Set User to Non Root
RUN adduser -s /bin/false cypress
RUN chown -R cypress:cypress ./
USER cypress
