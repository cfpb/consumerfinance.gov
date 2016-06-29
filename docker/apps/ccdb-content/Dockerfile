FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.cfpb.gov/CCDB4/CCDB-content.git /apps/ccdb-content/
RUN rm -rf /apps/ccdb-content/.git
RUN pip install -e /apps/ccdb-content
VOLUME /apps/ccdb-content
CMD echo "--- Installed ccdb content. ---"
