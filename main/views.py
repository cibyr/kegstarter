from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import DonationForm
from .models import Keg, Donation, Purchase

def home(request):
    total_donations = Donation.objects.all().aggregate(Sum('amount'))['amount__sum']
    if total_donations is None:
        total_donations = 0
    spent = Purchase.objects.all().aggregate(Sum('keg__price'))['keg__price__sum']
    if spent is None:
        spent = 0
    balance = total_donations - spent

    recent_kegs = Keg.objects.order_by('-added')[:3]
    context = {
        'kegs': recent_kegs,
        'total_donations': total_donations,
        'spent': spent,
        'balance': balance,
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    context = { 'form': form }
    return render(request, "registration/register.html", context)

@permission_required('main.accept_donation')
def accept_donation(request):
    new_donation = None
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            new_donation = form.save(commit=False)
            new_donation.recipient = request.user
            new_donation.save()
    form = DonationForm()
    context = { 'form': form, 'new_donation': new_donation }
    return render(request, 'donation.html', context)
