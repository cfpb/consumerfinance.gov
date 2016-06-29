FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.com/cfpb/regulations-core.git /apps/regulations-core/
RUN rm -rf /apps/regulations-core/.git
RUN pip install -e /apps/regulations-core
VOLUME /apps/regulations-core
CMD echo "--- Installed regulations core. ---"

