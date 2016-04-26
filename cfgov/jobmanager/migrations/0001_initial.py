# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApplicantType'
        db.create_table('jobmanager_applicanttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('applicant_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('jobmanager', ['ApplicantType'])

        # Adding model 'Grade'
        db.create_table('jobmanager_grade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('salary_min', self.gf('django.db.models.fields.IntegerField')()),
            ('salary_max', self.gf('django.db.models.fields.IntegerField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('jobmanager', ['Grade'])

        # Adding model 'JobCategory'
        db.create_table('jobmanager_jobcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('job_category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('blurb', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('jobmanager', ['JobCategory'])

        # Adding model 'Location'
        db.create_table('jobmanager_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('region_long', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('jobmanager', ['Location'])

        # Adding model 'Job'
        db.create_table('jobmanager_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobmanager.JobCategory'])),
            ('salary_min', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('salary_max', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('open_date', self.gf('django.db.models.fields.DateField')()),
            ('close_date', self.gf('django.db.models.fields.DateField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('jobmanager', ['Job'])

        # Adding M2M table for field grades on 'Job'
        db.create_table('jobmanager_job_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['jobmanager.job'], null=False)),
            ('grade', models.ForeignKey(orm['jobmanager.grade'], null=False))
        ))
        db.create_unique('jobmanager_job_grades', ['job_id', 'grade_id'])

        # Adding M2M table for field locations on 'Job'
        db.create_table('jobmanager_job_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['jobmanager.job'], null=False)),
            ('location', models.ForeignKey(orm['jobmanager.location'], null=False))
        ))
        db.create_unique('jobmanager_job_locations', ['job_id', 'location_id'])

        # Adding model 'JobApplicantType'
        db.create_table('jobmanager_jobapplicanttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobmanager.ApplicantType'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobmanager.Job'])),
            ('is_usajobs', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('usajobs_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('announcement_number', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('announcement_email', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('announcement_close_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('jobmanager', ['JobApplicantType'])


    def backwards(self, orm):
        # Deleting model 'ApplicantType'
        db.delete_table('jobmanager_applicanttype')

        # Deleting model 'Grade'
        db.delete_table('jobmanager_grade')

        # Deleting model 'JobCategory'
        db.delete_table('jobmanager_jobcategory')

        # Deleting model 'Location'
        db.delete_table('jobmanager_location')

        # Deleting model 'Job'
        db.delete_table('jobmanager_job')

        # Removing M2M table for field grades on 'Job'
        db.delete_table('jobmanager_job_grades')

        # Removing M2M table for field locations on 'Job'
        db.delete_table('jobmanager_job_locations')

        # Deleting model 'JobApplicantType'
        db.delete_table('jobmanager_jobapplicanttype')


    models = {
        'jobmanager.applicanttype': {
            'Meta': {'ordering': "['applicant_type']", 'object_name': 'ApplicantType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'applicant_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'jobmanager.grade': {
            'Meta': {'ordering': "['grade']", 'object_name': 'Grade'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salary_max': ('django.db.models.fields.IntegerField', [], {}),
            'salary_min': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'jobmanager.job': {
            'Meta': {'ordering': "['close_date', 'title']", 'object_name': 'Job'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'applicant_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobmanager.ApplicantType']", 'through': "orm['jobmanager.JobApplicantType']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobmanager.JobCategory']"}),
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobmanager.Grade']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jobmanager.Location']", 'symmetrical': 'False'}),
            'open_date': ('django.db.models.fields.DateField', [], {}),
            'salary_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'salary_min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'jobmanager.jobapplicanttype': {
            'Meta': {'ordering': "['job']", 'object_name': 'JobApplicantType'},
            'announcement_close_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'announcement_email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'announcement_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'application_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobmanager.ApplicantType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_usajobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobmanager.Job']"}),
            'usajobs_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'jobmanager.jobcategory': {
            'Meta': {'ordering': "['job_category']", 'object_name': 'JobCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'jobmanager.location': {
            'Meta': {'ordering': "['region']", 'object_name': 'Location'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'region_long': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['jobmanager']