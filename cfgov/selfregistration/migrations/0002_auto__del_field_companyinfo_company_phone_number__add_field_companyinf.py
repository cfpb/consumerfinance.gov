# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CompanyInfo.company_phone_number'
        db.delete_column(
            'selfregistration_companyinfo',
            'company_phone_number')

        # Adding field 'CompanyInfo.company_phone'
        db.add_column(
            'selfregistration_companyinfo',
            'company_phone',
            self.gf('localflavor.us.models.PhoneNumberField')(
                default='7175551212',
                max_length=20),
            keep_default=False)

        # Adding field 'CompanyInfo.submitted'
        db.add_column(
            'selfregistration_companyinfo',
            'submitted',
            self.gf('django.db.models.fields.DateTimeField')(
                auto_now_add=True,
                default=datetime.datetime(
                    2013,
                    5,
                    10,
                    0,
                    0),
                blank=True),
            keep_default=False)

        # Changing field 'CompanyInfo.website'
        db.alter_column('selfregistration_companyinfo', 'website', self.gf(
            'django.db.models.fields.URLField')(max_length=200, null=True))

    def backwards(self, orm):
        # Adding field 'CompanyInfo.company_phone_number'
        db.add_column(
            'selfregistration_companyinfo',
            'company_phone_number',
            self.gf('localflavor.us.models.PhoneNumberField')(
                default='http://google.com',
                max_length=20),
            keep_default=False)

        # Deleting field 'CompanyInfo.company_phone'
        db.delete_column('selfregistration_companyinfo', 'company_phone')

        # Deleting field 'CompanyInfo.submitted'
        db.delete_column('selfregistration_companyinfo', 'submitted')

        # User chose to not deal with backwards NULL issues for
        # 'CompanyInfo.website'
        raise RuntimeError(
            "Cannot reverse this migration. 'CompanyInfo.website' and its values cannot be restored.")

    models = {
        'selfregistration.companyinfo': {
            'Meta': {'object_name': 'CompanyInfo'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'contact_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tax_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['selfregistration']
