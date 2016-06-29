FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.cfpb.gov/CFPB/agreement_database.git /apps/agreement_database/
RUN rm -rf /apps/agreement_database/.git
RUN pip install -e /apps/agreement_database
VOLUME /apps/agreement_database
CMD echo "--- Installed agreement database. ---"
