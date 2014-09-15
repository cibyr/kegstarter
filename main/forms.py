from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelChoiceField, HiddenInput, IntegerField, EmailField
from .models import Donation, Vote, Purchase, Brewery, Keg, PaymentOption, Suggestion


class UserCreationWithEmailForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationWithEmailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class DonationForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.order_by('username'))

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

class PurchaseChangeForm(ModelForm):
    purchase_id = IntegerField(widget=HiddenInput())

    class Meta:
        model = Purchase
        fields = ['purchase_id', 'state']

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