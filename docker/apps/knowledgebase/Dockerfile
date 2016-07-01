FROM vickumar/python-nodejs

RUN git clone https://github.cfpb.gov/CFPB/knowledgebase.git /apps/knowledgebase/
RUN rm -rf /apps/knowledgebase/.git
RUN pip install -e /apps/knowledgebase
VOLUME /apps/knowledgebase
CMD echo "--- Installed knowledgebase. ---"

