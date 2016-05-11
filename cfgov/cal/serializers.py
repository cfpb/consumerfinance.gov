from rest_framework import serializers
from cal.models import CFPBCalendarEvent, CFPBCalendar

class CFPBCalendarEventSerializer(serializers.ModelSerializer):

	calendar = serializers.RelatedField(queryset=CFPBCalendar.objects.all())

	class Meta:
		model = CFPBCalendarEvent
