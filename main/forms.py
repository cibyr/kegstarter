from django.forms import ModelForm
from .models import Donation, Vote, Purchase

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
