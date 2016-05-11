# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CFPBCalendar'
        db.create_table(u'cal_cfpbcalendar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'cal', ['CFPBCalendar'])

        # Adding model 'CFPBCalendarEvent'
        db.create_table(u'cal_cfpbcalendarevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CFPBCalendar'])),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('dtstart', self.gf('django.db.models.fields.DateTimeField')()),
            ('dtend', self.gf('django.db.models.fields.DateTimeField')()),
            ('dtstamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recurrence_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cal', ['CFPBCalendarEvent'])


    def backwards(self, orm):
        # Deleting model 'CFPBCalendar'
        db.delete_table(u'cal_cfpbcalendar')

        # Deleting model 'CFPBCalendarEvent'
        db.delete_table(u'cal_cfpbcalendarevent')


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
        }
    }

    complete_apps = ['cal']