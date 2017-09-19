# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CompanyInfo.address'
        db.delete_column('selfregistration_companyinfo', 'address')

        # Adding field 'CompanyInfo.address1'
        db.add_column('selfregistration_companyinfo', 'address1',
                      self.gf('django.db.models.fields.CharField')(default='Address', max_length=1000),
                      keep_default=False)

        # Adding field 'CompanyInfo.address2'
        db.add_column('selfregistration_companyinfo', 'address2',
                      self.gf('django.db.models.fields.CharField')(default='address', max_length=1000),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CompanyInfo.address'
        raise RuntimeError("Cannot reverse this migration. 'CompanyInfo.address' and its values cannot be restored.")
        # Deleting field 'CompanyInfo.address1'
        db.delete_column('selfregistration_companyinfo', 'address1')

        # Deleting field 'CompanyInfo.address2'
        db.delete_column('selfregistration_companyinfo', 'address2')


    models = {
        'selfregistration.companyinfo': {
            'Meta': {'ordering': "['submitted']", 'object_name': 'CompanyInfo'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
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