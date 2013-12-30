from django.forms import ModelForm
from .models import Donation, Vote

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['user', 'amount']

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['keg', 'value']
