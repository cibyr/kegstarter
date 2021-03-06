# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Brewery.added_by'
        db.delete_column(u'main_brewery', 'added_by_id')

        # Adding field 'Brewery.image'
        db.add_column(u'main_brewery', 'image',
                      self.gf('django.db.models.fields.CharField')(max_length=2048, null=True),
                      keep_default=False)

        # Deleting field 'Keg.brewery'
        db.delete_column(u'main_keg', 'brewery_id')


        # Changing field 'Keg.image'
        db.alter_column(u'main_keg', 'image', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True))


        db.rename_column(u'main_untappdbrewery', 'brewery_id', '_brewery_id')

        db.rename_column(u'main_untappdkeg', 'keg_id', '_keg_id')

        db.rename_column(u'main_untappdkeg', 'brewery_id', 'untappd_brewery_id')


    def backwards(self, orm):
        # Adding field 'Brewery.added_by'
        db.add_column(u'main_brewery', 'added_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True),
                      keep_default=False)

        # Deleting field 'Brewery.image'
        db.delete_column(u'main_brewery', 'image')


        # User chose to not deal with backwards NULL issues for 'Keg.brewery'
        raise RuntimeError("Cannot reverse this migration. 'Keg.brewery' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Keg.brewery'
        db.add_column(u'main_keg', 'brewery',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Brewery']),
                      keep_default=False)


        # Changing field 'Keg.image'
        db.alter_column(u'main_keg', 'image', self.gf('django.db.models.fields.CharField')(default='', max_length=2048))

        db.rename_column(u'main_untappdbrewery', '_brewery_id', 'brewery_id')

        db.rename_column(u'main_untappdkeg', '_keg_id', 'keg_id')

        db.rename_column(u'main_untappdkeg', 'untappd_brewery_id', 'brewery_id')


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
            'image': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
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
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
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
            'price': ('main.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'proposed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'untappd_keg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.UntappdKeg']", 'null': 'True'})
        },
        u'main.untappdbrewery': {
            'Meta': {'object_name': 'UntappdBrewery'},
            '_brewery': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Brewery']", 'unique': 'True', 'null': 'True'}),
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
            '_keg': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Keg']", 'unique': 'True', 'null': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'untappd_brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.UntappdBrewery']"}),
            'untappd_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
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