# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationLocal'
        db.create_table(u'ip_assembler_locationlocal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('ip_assembler', ['LocationLocal'])


    def backwards(self, orm):
        # Deleting model 'LocationLocal'
        db.delete_table(u'ip_assembler_locationlocal')


    models = {
        'ip_assembler.ip': {
            'Meta': {'object_name': 'IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seg_0': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_1': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_2': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'seg_3': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'ip_assembler.locationlocal': {
            'Meta': {'object_name': 'LocationLocal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['ip_assembler']