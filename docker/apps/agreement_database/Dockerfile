FROM vickumar/python-nodejs

RUN git clone $AGREEMENT_DB_GIT /apps/agreement_database/
RUN rm -rf /apps/agreement_database/.git
RUN pip install -e /apps/agreement_database
VOLUME /apps/agreement_database
CMD echo "--- Installed agreement database. ---"
