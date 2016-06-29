FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.com/cfpb/regulations-site.git /apps/regulations-site/
RUN rm -rf /apps/regulations-site/.git
RUN pip install -e /apps/regulations-site
VOLUME /apps/regulations-site
CMD echo "--- Installed regulations site. ---"

