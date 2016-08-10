FROM vickumar/python-nodejs

RUN git clone $KNOWLEDGEBASE_GIT /apps/knowledgebase/
RUN rm -rf /apps/knowledgebase/.git
RUN pip install -e /apps/knowledgebase
VOLUME /apps/knowledgebase
CMD echo "--- Installed knowledgebase. ---"

