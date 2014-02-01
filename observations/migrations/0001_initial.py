# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Telescope'
        db.create_table('observations_telescope', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('observations', ['Telescope'])

        # Adding model 'Instrument'
        db.create_table('observations_instrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('telescope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Telescope'])),
        ))
        db.send_create_signal('observations', ['Instrument'])

        # Adding model 'Night'
        db.create_table('observations_night', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Instrument'])),
            ('ut_date', self.gf('django.db.models.fields.DateField')()),
            ('observers', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('log_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('observations', ['Night'])

        # Adding unique constraint on 'Night', fields ['instrument', 'ut_date']
        db.create_unique('observations_night', ['instrument_id', 'ut_date'])

        # Adding model 'Exposure'
        db.create_table('observations_exposure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('night', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Night'])),
            ('run_number', self.gf('django.db.models.fields.IntegerField')()),
            ('ut_start', self.gf('django.db.models.fields.TimeField')()),
            ('exposed', self.gf('django.db.models.fields.FloatField')()),
            ('ra', self.gf('django.db.models.fields.FloatField')()),
            ('dec', self.gf('django.db.models.fields.FloatField')()),
            ('object_exp', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('observations', ['Exposure'])

        # Adding unique constraint on 'Exposure', fields ['night', 'run_number']
        db.create_unique('observations_exposure', ['night_id', 'run_number'])

        # Adding model 'Query'
        db.create_table('observations_query', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('get_str', self.gf('django.db.models.fields.TextField')()),
            ('path', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('observations', ['Query'])

        # Adding model 'QueryInstance'
        db.create_table('observations_queryinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Query'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('observations', ['QueryInstance'])


    def backwards(self, orm):
        # Removing unique constraint on 'Exposure', fields ['night', 'run_number']
        db.delete_unique('observations_exposure', ['night_id', 'run_number'])

        # Removing unique constraint on 'Night', fields ['instrument', 'ut_date']
        db.delete_unique('observations_night', ['instrument_id', 'ut_date'])

        # Deleting model 'Telescope'
        db.delete_table('observations_telescope')

        # Deleting model 'Instrument'
        db.delete_table('observations_instrument')

        # Deleting model 'Night'
        db.delete_table('observations_night')

        # Deleting model 'Exposure'
        db.delete_table('observations_exposure')

        # Deleting model 'Query'
        db.delete_table('observations_query')

        # Deleting model 'QueryInstance'
        db.delete_table('observations_queryinstance')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'observations.exposure': {
            'Meta': {'unique_together': "(('night', 'run_number'),)", 'object_name': 'Exposure'},
            'dec': ('django.db.models.fields.FloatField', [], {}),
            'exposed': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'night': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['observations.Night']"}),
            'object_exp': ('django.db.models.fields.BooleanField', [], {}),
            'ra': ('django.db.models.fields.FloatField', [], {}),
            'run_number': ('django.db.models.fields.IntegerField', [], {}),
            'ut_start': ('django.db.models.fields.TimeField', [], {})
        },
        'observations.instrument': {
            'Meta': {'object_name': 'Instrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telescope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['observations.Telescope']"})
        },
        'observations.night': {
            'Meta': {'unique_together': "(('instrument', 'ut_date'),)", 'object_name': 'Night'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['observations.Instrument']"}),
            'log_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'observers': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ut_date': ('django.db.models.fields.DateField', [], {})
        },
        'observations.query': {
            'Meta': {'object_name': 'Query'},
            'get_str': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {})
        },
        'observations.queryinstance': {
            'Meta': {'object_name': 'QueryInstance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['observations.Query']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'observations.telescope': {
            'Meta': {'object_name': 'Telescope'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['observations']