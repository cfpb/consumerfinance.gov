FROM vickumar/python-nodejs

RUN git clone $OAH_GIT /apps/owning-a-home/
RUN git clone $TAX_TIME_SAVING_GIT /apps/tax-time-saving/
RUN rm -rf /apps/owning-a-home/.git
RUN rm -rf /apps/tax-time-saving/.git
VOLUME /apps/owning-a-home
VOLUME /apps/tax-time-saving
CMD echo "--- Installed sheer apps. ---"

