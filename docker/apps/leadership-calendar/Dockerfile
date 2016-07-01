FROM vickumar/python-nodejs

RUN git clone https://github.cfpb.gov/CFPB/leadership-calendar.git /apps/leadership-calendar/
RUN rm -rf /apps/leadership-calendar/.git
RUN pip install -e /apps/leadership-calendar
VOLUME /apps/leadership-calendar
CMD echo "--- Installed leadership calendar. ---"
