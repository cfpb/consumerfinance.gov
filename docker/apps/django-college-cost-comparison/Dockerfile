FROM vickumar/python-nodejs

RUN mkdir -p /apps
RUN git clone https://github.cfpb.gov/CFPB/django-college-cost-comparison.git /apps/django-college-cost-comparison/
RUN rm -rf /apps/django-college-cost-comparison/.git
RUN pip install -e /apps/django-college-cost-comparison
VOLUME /apps/django-college-cost-comparison
CMD echo "--- Installed django college cost comparison. ---"

