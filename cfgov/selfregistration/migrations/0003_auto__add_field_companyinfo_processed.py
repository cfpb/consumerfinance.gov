# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CompanyInfo.processed'
        db.add_column('selfregistration_companyinfo', 'processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CompanyInfo.processed'
        db.delete_column('selfregistration_companyinfo', 'processed')


    models = {
        'selfregistration.companyinfo': {
            'Meta': {'ordering': "['submitted']", 'object_name': 'CompanyInfo'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
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