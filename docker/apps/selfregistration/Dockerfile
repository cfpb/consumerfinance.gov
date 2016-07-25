FROM vickumar/python-nodejs

RUN git clone $SELFREGISTRATION_GIT /apps/selfregistration/
RUN rm -rf /apps/selfregistration/.git
RUN pip install -e /apps/selfregistration
VOLUME /apps/selfregistration
CMD echo "--- Installed leadership selfregistration. ---"

