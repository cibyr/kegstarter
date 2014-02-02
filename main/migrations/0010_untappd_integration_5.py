# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from ..api.untappd import *
from kegstarter.settings import *

class Migration(DataMigration):

    def try_add_bid(self, orm, bid):
        """
        @type bid: int
        """
        untappd_api = init_api()

        try:
            response = untappd_api.base_requester.GET(path="/beer/info/{}".format(bid))

            beer = response['beer']
            brewery = beer['brewery']

            # Look if we the brewery already
            try:
                untappd_brewery = orm.UntappdBrewery.objects.get(untappd_id=brewery['brewery_id'])
                print("* Using already made UntappdBrewery object")
            except ObjectDoesNotExist:
                untappd_brewery = orm.UntappdBrewery()
                untappd_brewery.untappd_id = brewery['brewery_id']
                untappd_brewery.save()
                print(u"* Creating new UntappdBrewery object ({})".format(brewery['brewery_name']))

            untappd_keg = orm.UntappdKeg()
            untappd_keg.untappd_id = beer['bid']
            untappd_keg.brewery = untappd_brewery
            untappd_keg.save()
            print(u"* Creating new UntappdKeg object ({})".format(beer['beer_name']))

            return untappd_keg
        except UntappdException:
            return None


    def forwards(self, orm):
        "Write your forwards methods here."
        # Cycle through each keg and grab its Untappd Beer ID

        print("**************************************")
        print("*     PLEASE LOOK UP EACH KEG ON     *")
        print("* UNTAPPD TO COMPLETE THIS MIGRATION *")
        print("**************************************")

        for keg in orm.Keg.objects.all():
            while True:
                done = True
                bid = None
                while not isinstance(bid, int):
                    # Ask for user input
                    try:
                        print("[Enter a negative number to remove suggestion (and all votes for it)]")
                        bid = input(u"Need Untappd Beer ID for {} - {}: ".format(keg.name, keg.brewery))

                    except Exception:
                        continue

                suggestion = orm.Suggestion.objects.get(keg=keg)

                if bid < 0:
                    try:
                        orm.Purchase.objects.get(suggestion=suggestion).delete()
                        print("* Purchase for suggestion found - deleted.")
                    except ObjectDoesNotExist:
                        print("* No purchase for suggestion found")

                    orm.Vote.objects.filter(suggestion=suggestion).delete()
                    print("* All votes for suggestion deleted")

                    suggestion.delete()
                    print("* Suggestion deleted")
                else:
                    # Store it in a UntappdKeg object, if we don't have one yet
                    try:
                        untappd_keg = orm.UntappdKeg.objects.get(untappd_id=bid)
                        print("* Using already made UntappdKeg object")
                    except ObjectDoesNotExist:
                        untappd_keg = self.try_add_bid(orm, bid)
                        if not untappd_keg:
                            print("* Not a valid Beer ID")
                            continue

                suggestion.untappd_keg = untappd_keg
                suggestion.keg = None
                suggestion.save()
                print("* Updated suggestion")

                # Delete the keg object
                keg.delete()
                print("* Deleting old Keg object")

                if done:
                    break

        print("Deleting all brewery objects...")
        # Then delete all brewery objects!
        orm.Brewery.objects.all().delete()
        print("* Done")

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration.")

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
            'brewery': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Brewery']", 'unique': 'True', 'null': 'True'}),
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
            'keg': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Keg']", 'unique': 'True', 'null': 'True'}),
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
    symmetrical = True
