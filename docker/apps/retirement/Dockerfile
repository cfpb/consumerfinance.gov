FROM vickumar/python-nodejs

RUN git clone $RETIREMENT_GIT /apps/retirement/
RUN rm -rf /apps/retirement/.git
RUN pip install -e /apps/retirement
VOLUME /apps/retirement
CMD echo "--- Installed retirement. ---"

