# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SpeakerVerification.user_code'
        db.add_column(u'iraqiSpeakerVerifiers_speakerverification', 'user_code',
                      self.gf('django.db.models.fields.CharField')(default='101e2a7f50b44e1981c3269e7aac3181', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SpeakerVerification.user_code'
        db.delete_column(u'iraqiSpeakerVerifiers_speakerverification', 'user_code')


    models = {
        u'iraqiSpeakerVerifiers.speakerverification': {
            'Meta': {'object_name': 'SpeakerVerification'},
            'answer1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer3': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer4': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer5': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answer6': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_code': ('django.db.models.fields.CharField', [], {'default': "'4fbf4b96b4e5418a854f6143df918df0'", 'max_length': '32'})
        }
    }

    complete_apps = ['iraqiSpeakerVerifiers']