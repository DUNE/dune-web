# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Individual.fax'
        db.add_column('members_individual', 'fax',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Individual.latex_name'
        db.add_column('members_individual', 'latex_name',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Institution.sort_name'
        db.add_column('members_institution', 'sort_name',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Institution.country'
        db.add_column('members_institution', 'country',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Individual.fax'
        db.delete_column('members_individual', 'fax')

        # Deleting field 'Individual.latex_name'
        db.delete_column('members_individual', 'latex_name')

        # Deleting field 'Institution.sort_name'
        db.delete_column('members_institution', 'sort_name')

        # Deleting field 'Institution.country'
        db.delete_column('members_institution', 'country')


    models = {
        'members.individual': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Individual'},
            'begin_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2008, 5, 1, 0, 0)', 'max_length': '50'}),
            'collaborator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'docdb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2038, 5, 1, 0, 0)', 'max_length': '50'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Institution']"}),
            'institution2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'institution2'", 'null': 'True', 'to': "orm['members.Institution']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'latex_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['members.Role']", 'symmetrical': 'False'})
        },
        'members.institution': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Institution'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'members.role': {
            'Meta': {'object_name': 'Role'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['members']