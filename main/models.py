from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.http import urlquote
from django.utils.encoding import iri_to_uri

from .fields import CurrencyField
from datetime import datetime, timedelta
from django.utils.timezone import utc

class UntappdModel(models.Model):
    untappd_id = models.IntegerField(primary_key=True)
    expires = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_default_expiry():
        return datetime.utcnow().replace(tzinfo=utc) + timedelta(days=1)

    class Meta:
        abstract = True


class Brewery(models.Model):
    #TODO: Proper Geo support?
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.CharField(max_length=2048, null=True)

    def __unicode__(self):
        return self.name


class UntappdBrewery(UntappdModel):
    _brewery = models.OneToOneField(Brewery, null=True)

    def brewery(self):
        if self._brewery is None:
            from main.api.untappd import cache_brewery
            self._brewery = cache_brewery(self)
            self.save()
            return self._brewery
        else:
            # TODO: Implement updating!
            return self._brewery

    def get_absolute_url(self):
        return iri_to_uri(u'/brewery/{}/{}'.format(self.pk,
            urlquote(slugify(unicode(self.brewery().name)))))


class Keg(models.Model):
    #TODO: tags?
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=200)
    desc = models.TextField(help_text='''Enter as much detail as you like,
        but be sure to at least include where we can purchase this keg.
        Markdown is supported for formatting.''')
    image = models.CharField(max_length=2048, null=True)
    rating = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name


class UntappdKeg(UntappdModel):
    untappd_brewery = models.ForeignKey(UntappdBrewery)
    _keg = models.OneToOneField(Keg, null=True)

    def keg(self):
        if self._keg is None:
            from main.api.untappd import cache_keg
            self._keg = cache_keg(self)
            self.save()
            return self._keg
        else:
            # TODO: Implement updating!
            return self._keg


class Suggestion(models.Model):
    untappd_keg = models.ForeignKey(UntappdKeg, null=True)
    gallons = models.FloatField(default=15.5,
            help_text='Size of the keg, in US gallons')
    price = CurrencyField(help_text='Cost to purchase this keg, in US dollars')
    proposed_by = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return iri_to_uri(u'/keg/{}/{}/{}'.format(self.pk,
                                       urlquote(slugify(unicode(self.untappd_keg.untappd_brewery.brewery().name))),
                                       urlquote(slugify(unicode(self.untappd_keg.keg().name)))))

    def votes(self):
        return self.vote_set.aggregate(Sum('value'))['value__sum'] or 0

    def __unicode__(self):
        return '{} ({} votes) - by {}'.format(self.untappd_keg.keg(), self.votes(), self.proposed_by)


class Donation(models.Model):
    class Meta:
        permissions = (
                ('accept_donation', 'Can accept donations'),
        )

    user = models.ForeignKey(User)
    amount = CurrencyField()
    recipient = models.ForeignKey(User, related_name='donations_received')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '${0.amount} from {0.user} to {0.recipient}'.format(self)


class Purchase(models.Model):
    user = models.ForeignKey(User)
    suggestion = models.OneToOneField(Suggestion)
    timestamp = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey(User)
    suggestion = models.ForeignKey(Suggestion)
    value = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0.value} votes by {0.user} for {0.suggestion}'.format(self)


class KegMaster(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField(auto_now_add=True)
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


class UntappdCredentials(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    token = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "untappd credentials"

    def __unicode__(self):
        return 'UntappdCredentials for {}'.format(self.user)
