# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        # Populate cal_cfpbpdffile table with existent pdf files
        old_files = [
            {'url':"http://files.consumerfinance.gov/f/rc_june2013.pdf",'title':'June 2013 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/f/sa_june2013.pdf",'title':'June 2013 (Steve Antonakes)'},
            {'url':"http://files.consumerfinance.gov/f/rc_may2013.pdf",'title':'May 2013 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/f/sa_may2013.pdf",'title':'May 2013 (Steve Antonakes)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_april2013.pdf",'title':'April 2013 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/sa_april2013.pdf",'title':'April 2013 (Steve Antonakes)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_march2013.pdf",'title':'March 2013 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/f/sa_march2013.pdf",'title':'March 2013 (Steve Antonakes)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_january2013.pdf",'title':'January 2013 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_january2013.pdf",'title':'January 2013 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_december2012.pdf",'title':'December 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_december2012.pdf",'title':'December 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_november2012.pdf",'title':'November 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_november2012.pdf",'title':'November 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_october2012.pdf",'title':'October 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_october2012.pdf",'title':'October 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_september2012.pdf",'title':'September 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_september2012.pdf",'title':'September 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_august2012.pdf",'title':'August 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_august2012.pdf",'title':'August 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_july2012.pdf",'title':'July 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_july2012.pdf",'title':'July 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_june2012.pdf",'title':'June 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_june2012.pdf",'title':'June 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_may2012.pdf",'title':'May 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_may2012.pdf",'title':'May 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_april2012.pdf",'title':'April 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_april2012.pdf",'title':'April 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rc_march2012.pdf",'title':'March 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/a/assets/calendar/rd_march2012.pdf",'title':'March 2012 (Raj Date)'},
            {'url':"http://files.consumerfinance.gov/f/2012/02/RC_Calendar_JanFeb_2012_Final.pdf",'title':'January-February 2012 (Richard Cordray)'},
            {'url':"http://files.consumerfinance.gov/f/2012/02/RD_Calendar_JanFeb_2012_Final.pdf",'title':'January-February 2012 (Raj Date)'},
            {'url':"/wp-content/uploads/2012/01/RD_Calendar_December_2011-Final.pdf",'title':'December 2011'},
            {'url':"/wp-content/uploads/2011/12/RD_Calendar_November_2011-Final.pdf",'title':'November 2011'},
            {'url':"/wp-content/uploads/2011/11/RD_Calendar_October_2011-Final.pdf",'title':'October 2011'},
            {'url':"/wp-content/uploads/2011/10/RD_Calendar_September_2011-Final.pdf",'title':'September 2011'},
            {'url':"/wp-content/uploads/2011/09/RD_Calendar_August-Final.pdf",'title':'August 2011'},
            {'url':"/wp-content/uploads/2011/08/EW_Calendar_July-Final.pdf",'title':'July 2011'},
            {'url':"/wp-content/uploads/2011/07/EW_Calendar_June-Final.pdf",'title':'June 2011'},
            {'url':"/wp-content/uploads/2011/07/EW_Calendar_May-Final.pdf",'title':'May 2011'},
            {'url':"/wp-content/uploads/2010/12/EW_Calendar_April-Final.pdf",'title':'April 2011'},
            {'url':"/wp-content/uploads/2011/04/EW_Calendar_March-2011.pdf",'title':'March 2011'},
            {'url':"/wp-content/uploads/2011/03/EW_Calendar_Feb_2011.pdf",'title':'February 2011'},
            {'url':"/wp-content/uploads/2011/02/EW_Calendar_Jan_2011.pdf",'title':'January 2011'},
            {'url':"/wp-content/uploads/2011/03/EW_Calendar_Dec_2010.pdf",'title':'December 2010'},
            {'url':"/wp-content/uploads/2011/03/EW_Calendar_Nov_2010.pdf",'title':'November 2010'},
            {'url':"/wp-content/uploads/2011/03/EW_Calendar_Sept-Oct_2010.pdf",'title':'September-October 2010'},
        ]

        # need to reverse old_files because we'll show files in select ordered by -id
        for file in reversed(old_files):
            obj = orm['cal.cfpbpdffile']()
            obj.url = file['url']
            obj.title = file['title']
            obj.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        u'cal.cfpbcalendar': {
            'Meta': {'object_name': 'CFPBCalendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'cal.cfpbcalendarevent': {
            'Meta': {'object_name': 'CFPBCalendarEvent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cal.CFPBCalendar']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dtend': ('django.db.models.fields.DateTimeField', [], {}),
            'dtstamp': ('django.db.models.fields.DateTimeField', [], {}),
            'dtstart': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'recurrence_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'cal.cfpbpdffile': {
            'Meta': {'object_name': 'CFPBPDFFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['cal']
    symmetrical = True
