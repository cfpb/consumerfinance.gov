FROM vickumar/python-nodejs

RUN git clone $PICARD_GIT /apps/picard/
RUN rm -rf /apps/picard/.git
RUN pip install -e /apps/picard
VOLUME /apps/picard
CMD echo "--- Installed picard. ---"
