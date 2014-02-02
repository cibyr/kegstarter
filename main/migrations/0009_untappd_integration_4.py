# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UntappdBrewery'
        db.create_table(u'main_untappdbrewery', (
            ('untappd_id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(auto_now=True)),
            ('brewery', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Brewery'], null=True)),
        ))
        db.send_create_signal(u'main', ['UntappdBrewery'])

        # Adding model 'UntappdKeg'
        db.create_table(u'main_untappdkeg', (
            ('untappd_id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(auto_now=True)),
            ('keg', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Keg'], null=True)),
            ('brewery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.UntappdBrewery'])),
        ))
        db.send_create_signal(u'main', ['UntappdKeg'])

        # Adding field 'Suggestion.untappd_keg'
        db.add_column(u'main_suggestion', 'untappd_keg',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.UntappdKeg'], null=True),
                      keep_default=False)

        # Changing field 'Suggestion.keg'
        db.alter_column(u'main_suggestion', 'keg_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Keg'], null=True))


    def backwards(self, orm):
        # Changing field 'Suggestion.keg'
        db.alter_column(u'main_suggestion', 'keg_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Keg']))

        # Deleting field 'Suggestion.untappd_keg'
        db.delete_column(u'main_suggestion', 'untappd_keg_id')

        # Deleting model 'UntappdKeg'
        db.delete_table(u'main_untappdkeg')

        # Deleting model 'UntappdBrewery'
        db.delete_table(u'main_untappdbrewery')

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
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
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
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Brewery']"}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'main.kegmaster': {
            'Meta': {'object_name': 'KegMaster'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.paymentoption': {
            'Meta': {'object_name': 'PaymentOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'preferred': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'main.purchase': {
            'Meta': {'object_name': 'Purchase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suggestion': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Suggestion']", 'unique': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'gallons': ('django.db.models.fields.FloatField', [], {'default': '15.5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Keg']", 'null': 'True'}),
            'price': ('main.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'untappd_keg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.UntappdKeg']", 'null': 'True'})
        },
        u'main.untappdbrewery': {
            'Meta': {'object_name': 'UntappdBrewery'},
            'brewery': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Brewery']", 'null': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'untappd_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'main.untappdcredentials': {
            'Meta': {'object_name': 'UntappdCredentials'},
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'main.untappdkeg': {
            'Meta': {'object_name': 'UntappdKeg'},
            'expires': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'keg': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Keg']", 'null': 'True'}),
            'untappd_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.UntappdBrewery']"})
        },
        u'main.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suggestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Suggestion']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['main']