from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.text import slugify

from .fields import CurrencyField

class Brewery(models.Model):
    #TODO: Proper Geo support?
    #TODO: images
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    desc = models.TextField()
    added_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/brewery/{}/{}'.format(self.pk, slugify(self.name))

class Keg(models.Model):
    #TODO: images
    #TODO: tags?
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=200)
    brewery = models.ForeignKey('Brewery', related_name='kegs')
    gallons = models.FloatField(default=15.5,
            help_text='Size of the keg, in US gallons')
    price = CurrencyField(help_text='Cost to purchase this keg, in US dollars')
    desc = models.TextField(help_text='''Enter as much detail as you like,
        but be sure to at least include where we can purchase this keg.
        Markdown is supported for formatting.''')
    added = models.DateTimeField(auto_now=True)
    proposed_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        str_list = [self.name]
        if self.style:
            str_list.append(' ({0.style})'.format(self))
        if self.brewery.name:
            str_list.append(' - {0}'.format(self.brewery.name))
        return ''.join(str_list)

    def get_absolute_url(self):
        return '/keg/{}/{}/{}'.format(self.pk, slugify(self.brewery.name), slugify(self.name))

    def votes(self):
        return self.vote_set.aggregate(Sum('value'))['value__sum'] or 0

class Donation(models.Model):
    class Meta:
        permissions = (
                ('accept_donation', 'Can accept donations'),
        )

    user = models.ForeignKey(User)
    amount = CurrencyField()
    recipient = models.ForeignKey(User, related_name='donations_received')
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '${0.amount} from {0.user} to {0.recipient}'.format(self)

class Purchase(models.Model):
    user = models.ForeignKey(User)
    keg = models.OneToOneField(Keg)
    timestamp = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    user = models.ForeignKey(User)
    keg = models.ForeignKey(Keg)
    value = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0.value} votes by {0.user} for {0.keg}'.format(self)

class KegMaster(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '{0.user} is keg master from {0.start} to {0.end}'.format(self)


class PaymentOption(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    info = models.CharField(max_length=200, blank=True)
    preferred = models.BooleanField()

    def __unicode__(self):
        return '{0.user}: {0.name} = {0.value} ({0.info})'.format(self)