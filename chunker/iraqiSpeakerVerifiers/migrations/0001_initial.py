# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Answer1'
        db.create_table(u'iraqiSpeakerVerifiers_answer1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'iraqiSpeakerVerifiers', ['Answer1'])


    def backwards(self, orm):
        # Deleting model 'Answer1'
        db.delete_table(u'iraqiSpeakerVerifiers_answer1')


    models = {
        u'iraqiSpeakerVerifiers.answer1': {
            'Meta': {'object_name': 'Answer1'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['iraqiSpeakerVerifiers']