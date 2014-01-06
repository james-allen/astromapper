# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Instrument'
        db.create_table('observations_instrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('telescope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Telescope'])),
        ))
        db.send_create_signal('observations', ['Instrument'])

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

        # Adding model 'Telescope'
        db.create_table('observations_telescope', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('observations', ['Telescope'])


    def backwards(self, orm):
        # Removing unique constraint on 'Night', fields ['instrument', 'ut_date']
        db.delete_unique('observations_night', ['instrument_id', 'ut_date'])

        # Removing unique constraint on 'Exposure', fields ['night', 'run_number']
        db.delete_unique('observations_exposure', ['night_id', 'run_number'])

        # Deleting model 'Instrument'
        db.delete_table('observations_instrument')

        # Deleting model 'Exposure'
        db.delete_table('observations_exposure')

        # Deleting model 'Night'
        db.delete_table('observations_night')

        # Deleting model 'Telescope'
        db.delete_table('observations_telescope')


    models = {
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
        'observations.telescope': {
            'Meta': {'object_name': 'Telescope'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['observations']