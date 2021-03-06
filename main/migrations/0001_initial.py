# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brewery'
        db.create_table(u'main_brewery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Brewery'])

        # Adding model 'Keg'
        db.create_table(u'main_keg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('brewery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Brewery'])),
            ('gallons', self.gf('django.db.models.fields.FloatField')(default=15.5)),
            ('price', self.gf('main.fields.CurrencyField')(max_digits=10, decimal_places=2)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Keg'])

        # Adding model 'Donation'
        db.create_table(u'main_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('amount', self.gf('main.fields.CurrencyField')(max_digits=10, decimal_places=2)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donations_received', to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Donation'])

        # Adding model 'Purchase'
        db.create_table(u'main_purchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('keg', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Keg'], unique=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Purchase'])

        # Adding model 'Vote'
        db.create_table(u'main_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('keg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Keg'])),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Brewery'
        db.delete_table(u'main_brewery')

        # Deleting model 'Keg'
        db.delete_table(u'main_keg')

        # Deleting model 'Donation'
        db.delete_table(u'main_donation')

        # Deleting model 'Purchase'
        db.delete_table(u'main_purchase')

        # Deleting model 'Vote'
        db.delete_table(u'main_vote')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.brewery': {
            'Meta': {'object_name': 'Brewery'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'main.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('main.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donations_received'", 'to': u"orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.keg': {
            'Meta': {'object_name': 'Keg'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Brewery']"}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'gallons': ('django.db.models.fields.FloatField', [], {'default': '15.5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('main.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'main.purchase': {
            'Meta': {'object_name': 'Purchase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Keg']", 'unique': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Keg']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['main']