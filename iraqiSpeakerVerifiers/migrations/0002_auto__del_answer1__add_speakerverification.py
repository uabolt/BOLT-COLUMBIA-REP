# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Answer1'
        db.delete_table(u'iraqiSpeakerVerifiers_answer1')

        # Adding model 'SpeakerVerification'
        db.create_table(u'iraqiSpeakerVerifiers_speakerverification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer3', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer4', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer5', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer6', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'iraqiSpeakerVerifiers', ['SpeakerVerification'])


    def backwards(self, orm):
        # Adding model 'Answer1'
        db.create_table(u'iraqiSpeakerVerifiers_answer1', (
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'iraqiSpeakerVerifiers', ['Answer1'])

        # Deleting model 'SpeakerVerification'
        db.delete_table(u'iraqiSpeakerVerifiers_speakerverification')


    models = {
        u'iraqiSpeakerVerifiers.speakerverification': {
            'Meta': {'object_name': 'SpeakerVerification'},
            'answer1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer3': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer4': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer5': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer6': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['iraqiSpeakerVerifiers']