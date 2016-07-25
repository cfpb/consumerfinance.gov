FROM vickumar/python-nodejs

RUN git clone $EREGS_GIT /apps/eregs/
RUN rm -rf /apps/eregs/.git
RUN pip install -e /apps/eregs
VOLUME /apps/eregs
CMD echo "--- Installed eregs. ---"
