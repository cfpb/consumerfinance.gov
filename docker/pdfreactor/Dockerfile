FROM cfgov/base
WORKDIR /opt/

RUN curl http://download.realobjects.de/PDFreactor_6_3_6828_3_unix_installer.tar.gz \
    | tar -xz
RUN yum -y install java-1.7.0-openjdk  && yum clean all

EXPOSE 9423

# make sure error.log exists before we start tailing it
RUN touch PDFreactor/bin/error.log
ADD pdfreactorwebservice.vmoptions /opt/PDFreactor/bin/

# removes the line that locks Jetty down to only serving on localhost
RUN awk '!/localhost/' /opt/PDFreactor/jetty/etc/jetty.xml  > temp && \
    mv temp /opt/PDFreactor/jetty/etc/jetty.xml

VOLUME /opt/PDFreactor/wrappers/python/lib
CMD /opt/PDFreactor/bin/pdfreactorwebservice start\
    && tail -f /opt/PDFreactor/bin/error.log
