from django.db import models
from django.forms import ModelForm
from .models import Donation, Vote, Purchase, Brewery, Keg, PaymentOption

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['user', 'amount']

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['keg', 'value']

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['keg']

class PurchasePriceForm(ModelForm):
    class Meta:
        model = Keg
        fields = ['price']

class BreweryForm(ModelForm):
    class Meta:
        model = Brewery
        exclude = ['added_by']

class KegForm(ModelForm):
    class Meta:
        model = Keg
        exclude = ['proposed_by']


class AddPaymentOptionForm(ModelForm):
    class Meta:
        model = PaymentOption
        exclude = ['user']