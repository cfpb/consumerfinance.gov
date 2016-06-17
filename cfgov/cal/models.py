from django.db import models
import uuid


class CFPBCalendar(models.Model):
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.title)

class CFPBCalendarEvent(models.Model):
    calendar = models.ForeignKey(CFPBCalendar)
    uid = models.CharField(max_length=255, blank=True)
    dtstart = models.DateTimeField()
    dtend = models.DateTimeField()
    dtstamp = models.DateTimeField()
    sequence = models.IntegerField(default=0)
    recurrence_id = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(blank=True)
    all_day = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    @property
    def day(self):
        return self.dtstart.date()

    def save(self):
        if self.uid == None or self.uid == "":
            self.uid = uuid.uuid4()
        super(CFPBCalendarEvent, self).save()

    def __unicode__(self):
        return "%s: %s (%s)" % (self.dtstart, self.summary, self.location)


class CFPBImportICSFile(CFPBCalendar):
    class Meta:
        proxy = True

    def __unicode__(self):
        return "%s" % ("CFPB Import ICS File")
