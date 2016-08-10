FROM vickumar/python-nodejs

RUN git clone $DJANGO_HUD_GIT /apps/django-hud/
RUN rm -rf /apps/django-hud/.git
CMD pip install -e /apps/django-hud
VOLUME /apps/django-hud
CMD echo "--- Installed django hud. ---"
