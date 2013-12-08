from django.db import models
from django.contrib.auth.models import User

from .fields import CurrencyField

class Brewery(models.Model):
    #TODO: Proper Geo support?
    #TODO: images
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    desc = models.TextField()

    def __unicode__(self):
        return self.name

class Keg(models.Model):
    #TODO: images
    #TODO: tags?
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=200)
    brewery = models.ForeignKey('Brewery')
    gallons = models.FloatField(default=15.5,
            help_text='Size of the keg, in US gallons')
    price = CurrencyField(help_text='Cost to purchase this keg, in US dollars')
    desc = models.TextField()
    added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Donation(models.Model):
    user = models.ForeignKey(User)
    amount = CurrencyField()
    recipient = models.ForeignKey(User, related_name='donations_received')
    timestamp = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    user = models.ForeignKey(User)
    keg = models.OneToOneField(Keg)
    timestamp = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    user = models.ForeignKey(User)
    keg = models.ForeignKey(Keg)
    value = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now=True)