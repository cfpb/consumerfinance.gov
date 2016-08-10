FROM vickumar/python-nodejs

RUN git clone https://github.com/cfpb/owning-a-home /apps/owning-a-home/
RUN git clone https://github.com/cfpb/tax-time-saving /apps/tax-time-saving/
RUN rm -rf /apps/owning-a-home/.git
RUN rm -rf /apps/tax-time-saving/.git
VOLUME /apps/owning-a-home
VOLUME /apps/tax-time-saving
CMD echo "--- Installed sheer apps. ---"

