# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationFTP'
        db.create_table(u'ip_assembler_locationftp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django_fields.fields.EncryptedCharField')(max_length=110, block_type='MODE_CBC', cipher='AES')),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('ip_assembler', ['LocationFTP'])


    def backwards(self, orm):
        # Deleting model 'LocationFTP'
        db.delete_table(u'ip_assembler_locationftp')


    models = {
        'ip_assembler.ip': {
            'Meta': {'object_name': 'IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seg_0': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_1': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_2': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_3': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'ip_assembler.locationftp': {
            'Meta': {'object_name': 'LocationFTP'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django_fields.fields.EncryptedCharField', [], {'max_length': '110', 'block_type': "'MODE_CBC'", 'cipher': "'AES'"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ip_assembler.locationlocal': {
            'Meta': {'object_name': 'LocationLocal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['ip_assembler']