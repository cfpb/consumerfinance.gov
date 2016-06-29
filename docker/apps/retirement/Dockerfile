FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.com/cfpb/retirement.git /apps/retirement/
RUN rm -rf /apps/retirement/.git
RUN pip install -e /apps/retirement
VOLUME /apps/retirement
CMD echo "--- Installed retirement. ---"

