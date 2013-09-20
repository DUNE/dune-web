# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table('members_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('members', ['Role'])

        # Adding model 'Institution'
        db.create_table('members_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('members', ['Institution'])

        # Adding model 'Individual'
        db.create_table('members_individual', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('collaborator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('begin_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2008, 5, 1, 0, 0), max_length=50)),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2038, 5, 1, 0, 0), max_length=50)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Institution'])),
        ))
        db.send_create_signal('members', ['Individual'])

        # Adding M2M table for field role on 'Individual'
        m2m_table_name = db.shorten_name('members_individual_role')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('individual', models.ForeignKey(orm['members.individual'], null=False)),
            ('role', models.ForeignKey(orm['members.role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['individual_id', 'role_id'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table('members_role')

        # Deleting model 'Institution'
        db.delete_table('members_institution')

        # Deleting model 'Individual'
        db.delete_table('members_individual')

        # Removing M2M table for field role on 'Individual'
        db.delete_table(db.shorten_name('members_individual_role'))


    models = {
        'members.individual': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Individual'},
            'begin_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2008, 5, 1, 0, 0)', 'max_length': '50'}),
            'collaborator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2038, 5, 1, 0, 0)', 'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Institution']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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