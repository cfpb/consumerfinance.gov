# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Grade', fields ['slug']
        db.delete_unique('jobmanager_grade', ['slug'])

        # Removing unique constraint on 'Job', fields ['slug']
        db.delete_unique('jobmanager_job', ['slug'])

        # Removing unique constraint on 'JobCategory', fields ['slug']
        db.delete_unique('jobmanager_jobcategory', ['slug'])

        # Removing unique constraint on 'ApplicantType', fields ['slug']
        db.delete_unique('jobmanager_applicanttype', ['slug'])

        # Removing unique constraint on 'Location', fields ['slug']
        db.delete_unique('jobmanager_location', ['slug'])


        # Changing field 'Location.slug'
        db.alter_column('jobmanager_location', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Adding index on 'Location', fields ['slug']
        db.create_index('jobmanager_location', ['slug'])


        # Changing field 'ApplicantType.slug'
        db.alter_column('jobmanager_applicanttype', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Adding index on 'ApplicantType', fields ['slug']
        db.create_index('jobmanager_applicanttype', ['slug'])


        # Changing field 'JobCategory.slug'
        db.alter_column('jobmanager_jobcategory', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Adding index on 'JobCategory', fields ['slug']
        db.create_index('jobmanager_jobcategory', ['slug'])


        # Changing field 'Job.slug'
        db.alter_column('jobmanager_job', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Adding index on 'Job', fields ['slug']
        db.create_index('jobmanager_job', ['slug'])


        # Changing field 'Grade.slug'
        db.alter_column('jobmanager_grade', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Adding index on 'Grade', fields ['slug']
        db.create_index('jobmanager_grade', ['slug'])


    def backwards(self, orm):
        # Removing index on 'Grade', fields ['slug']
        db.delete_index('jobmanager_grade', ['slug'])

        # Removing index on 'Job', fields ['slug']
        db.delete_index('jobmanager_job', ['slug'])

        # Removing index on 'JobCategory', fields ['slug']
        db.delete_index('jobmanager_jobcategory', ['slug'])

        # Removing index on 'ApplicantType', fields ['slug']
        db.delete_index('jobmanager_applicanttype', ['slug'])

        # Removing index on 'Location', fields ['slug']
        db.delete_index('jobmanager_location', ['slug'])


        # Changing field 'Location.slug'
        db.alter_column('jobmanager_location', 'slug', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))
        # Adding unique constraint on 'Location', fields ['slug']
        db.create_unique('jobmanager_location', ['slug'])


        # Changing field 'ApplicantType.slug'
        db.alter_column('jobmanager_applicanttype', 'slug', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))
        # Adding unique constraint on 'ApplicantType', fields ['slug']
        db.create_unique('jobmanager_applicanttype', ['slug'])


        # Changing field 'JobCategory.slug'
        db.alter_column('jobmanager_jobcategory', 'slug', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))
        # Adding unique constraint on 'JobCategory', fields ['slug']
        db.create_unique('jobmanager_jobcategory', ['slug'])


        # Changing field 'Job.slug'
        db.alter_column('jobmanager_job', 'slug', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))
        # Adding unique constraint on 'Job', fields ['slug']
        db.create_unique('jobmanager_job', ['slug'])


        # Changing field 'Grade.slug'
        db.alter_column('jobmanager_grade', 'slug', self.gf('django.db.models.fields.CharField')(max_length=128, unique=True))
        # Adding unique constraint on 'Grade', fields ['slug']
        db.create_unique('jobmanager_grade', ['slug'])


    models = {
        'jobmanager.applicanttype': {
            'Meta': {'ordering': "['applicant_type']", 'object_name': 'ApplicantType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'applicant_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'jobmanager.grade': {
            'Meta': {'ordering': "['grade']", 'object_name': 'Grade'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salary_max': ('django.db.models.fields.IntegerField', [], {}),
            'salary_min': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'jobmanager.location': {
            'Meta': {'ordering': "['region']", 'object_name': 'Location'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'region_long': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['jobmanager']