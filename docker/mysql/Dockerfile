FROM cfgov/base

RUN yum -y install mysql-server && yum clean all
RUN mysql_install_db
RUN /etc/init.d/mysqld start && sleep 10 && \
    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql mysql &&\
     /etc/init.d/mysqld stop
EXPOSE 3306
VOLUME /var/lib/mysql

CMD ["mysqld_safe", "--skip-grant-tables"]
