FROM vickumar/python-nodejs

RUN git clone $COLLEGE_COSTS_GIT /apps/college-costs/
RUN rm -rf /apps/college-costs/.git
RUN pip install -e /apps/college-costs
VOLUME /apps/college-costs
CMD echo "--- Installed college costs. ---"
