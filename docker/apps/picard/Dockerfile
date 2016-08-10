FROM vickumar/python-nodejs

RUN git clone https://github.cfpb.gov/CFPB/Picard /apps/picard/
RUN rm -rf /apps/picard/.git
RUN pip install -e /apps/picard
VOLUME /apps/picard
CMD echo "--- Installed picard. ---"
