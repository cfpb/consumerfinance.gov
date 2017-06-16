# This is a bandwidth-saving hack:
FROM elasticsearch:2.3
WORKDIR /opt/

RUN curl http://download.realobjects.de/PDFreactor_6_3_6828_3_unix_installer.tar.gz \
    | tar -xz

EXPOSE 9423

# make sure error.log exists before we start tailing it
RUN touch PDFreactor/bin/error.log
ADD pdfreactorwebservice.vmoptions /opt/PDFreactor/bin/

# removes the line that locks Jetty down to only serving on localhost
RUN awk '!/localhost/' /opt/PDFreactor/jetty/etc/jetty.xml  > temp && \
    mv temp /opt/PDFreactor/jetty/etc/jetty.xml

CMD /opt/PDFreactor/bin/pdfreactorwebservice start\
    && tail -f /opt/PDFreactor/bin/error.log
