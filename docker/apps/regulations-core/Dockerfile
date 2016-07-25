FROM vickumar/python-nodejs

RUN git clone $REG_CORE_GIT /apps/regulations-core/
RUN rm -rf /apps/regulations-core/.git
RUN pip install -e /apps/regulations-core
VOLUME /apps/regulations-core
CMD echo "--- Installed regulations core. ---"

