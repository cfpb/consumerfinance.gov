FROM vickumar/python-nodejs

RUN git clone $OAH_API_GIT /apps/owning-a-home-api/
RUN rm -rf /apps/owning-a-home-api/.git
RUN pip install -e /apps/owning-a-home-api
VOLUME /apps/owning-a-home-api
CMD echo "--- Installed owning a home api. ---"

