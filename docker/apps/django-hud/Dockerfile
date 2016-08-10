FROM vickumar/python-nodejs

RUN git clone https://github.com/cfpb/django-hud.git /apps/django-hud/
RUN rm -rf /apps/django-hud/.git
CMD pip install -e /apps/django-hud
VOLUME /apps/django-hud
CMD echo "--- Installed django hud. ---"
