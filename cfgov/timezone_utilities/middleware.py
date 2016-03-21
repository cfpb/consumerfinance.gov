import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
    	 # Be explicit that this ET is the timezone we are assuming admins are in,
    	 # Otherwise, TODO: Grab tzname from user 
        tzname = 'US/Eastern'
        timezone.activate(pytz.timezone(tzname))
