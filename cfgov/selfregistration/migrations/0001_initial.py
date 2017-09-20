# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyInfo'
        db.create_table('selfregistration_companyinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('tax_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('company_phone_number', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('contact_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contact_phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
        ))
        db.send_create_signal('selfregistration', ['CompanyInfo'])

    def backwards(self, orm):
        # Deleting model 'CompanyInfo'
        db.delete_table('selfregistration_companyinfo')

    models = {
        'selfregistration.companyinfo': {
            'Meta': {'object_name': 'CompanyInfo'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'company_phone_number': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'contact_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'contact_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'tax_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['selfregistration']
