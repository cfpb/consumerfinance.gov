# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CompanyInfo.contact_ext'
        db.add_column('selfregistration_companyinfo', 'contact_ext',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CompanyInfo.contact_ext'
        db.delete_column('selfregistration_companyinfo', 'contact_ext')


    models = {
        'selfregistration.companyinfo': {
            'Meta': {'ordering': "['submitted']", 'object_name': 'CompanyInfo'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_ext': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'contact_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tax_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['selfregistration']