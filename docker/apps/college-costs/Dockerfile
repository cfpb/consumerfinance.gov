FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.com/cfpb/college-costs /apps/college-costs/
RUN rm -rf /apps/college-costs/.git
RUN pip install -e /apps/college-costs
VOLUME /apps/college-costs
CMD echo "--- Installed college costs. ---"
