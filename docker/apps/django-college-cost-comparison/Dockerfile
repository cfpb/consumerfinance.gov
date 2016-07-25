FROM vickumar/python-nodejs

RUN git clone $COST_COMPARISON_GIT /apps/django-college-cost-comparison/
RUN rm -rf /apps/django-college-cost-comparison/.git
RUN pip install -e /apps/django-college-cost-comparison
VOLUME /apps/django-college-cost-comparison
CMD echo "--- Installed django college cost comparison. ---"

