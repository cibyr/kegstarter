from django.db import models
from django.forms import ModelForm
from .models import Donation, Vote, Purchase, Brewery, Keg, PaymentOption, Suggestion

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['user', 'amount']

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['suggestion', 'value']

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['suggestion']

class PurchasePriceForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['price']

class KegForm(ModelForm):
    class Meta:
        model = Keg
        exclude = ['proposed_by']


class AddPaymentOptionForm(ModelForm):
    class Meta:
        model = PaymentOption
        exclude = ['user']


class DeletePaymentOptionForm(ModelForm):
    class Meta:
        model = PaymentOption
        fields = ['id']