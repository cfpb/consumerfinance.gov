FROM vickumar/python-nodejs

RUN git clone https://github.cfpb.gov/CFPB/cfgov-selfregistration.git /apps/selfregistration/
RUN rm -rf /apps/selfregistration/.git
RUN pip install -e /apps/selfregistration
VOLUME /apps/selfregistration
CMD echo "--- Installed leadership selfregistration. ---"

