# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Individual.email2'
        db.add_column('members_individual', 'email2',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Individual.email2'
        db.delete_column('members_individual', 'email2')


    models = {
        'members.individual': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Individual'},
            'begin_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2008, 5, 1, 0, 0)', 'max_length': '50'}),
            'collaborator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'docdb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2038, 5, 1, 0, 0)', 'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Institution']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nick': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['members.Role']", 'symmetrical': 'False'})
        },
        'members.institution': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Institution'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'members.role': {
            'Meta': {'object_name': 'Role'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['members']