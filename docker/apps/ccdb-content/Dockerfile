FROM vickumar/python-nodejs

RUN git clone $CCDB_GIT /apps/ccdb-content/
RUN rm -rf /apps/ccdb-content/.git
RUN pip install -e /apps/ccdb-content
VOLUME /apps/ccdb-content
CMD echo "--- Installed ccdb content. ---"
