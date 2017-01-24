FROM cfgov/base

RUN yum -y install epel-release php php-mysql httpd && yum install -y phpmyadmin\
    && yum clean all

EXPOSE 80

ADD php.ini /etc/
ADD config.inc.php /etc/phpMyAdmin/
ADD phpMyAdmin.conf /etc/httpd/conf.d/
RUN chmod +r /etc/phpMyAdmin/config.inc.php

CMD apachectl -D FOREGROUND
