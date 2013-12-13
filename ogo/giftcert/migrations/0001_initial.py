# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GiftCert'
        db.create_table(u'giftcert_giftcert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('from_phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('order_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('staff_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('applied_to_account', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmation_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'giftcert', ['GiftCert'])


    def backwards(self, orm):
        # Deleting model 'GiftCert'
        db.delete_table(u'giftcert_giftcert')


    models = {
        u'giftcert.giftcert': {
            'Meta': {'ordering': "('-order_date',)", 'object_name': 'GiftCert'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'applied_to_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmation_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'from_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'staff_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['giftcert']