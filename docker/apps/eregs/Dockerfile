FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.cfpb.gov/eregs/ip.git /apps/eregs/
RUN rm -rf /apps/eregs/.git
RUN pip install -e /apps/eregs
VOLUME /apps/eregs
CMD echo "--- Installed eregs. ---"
