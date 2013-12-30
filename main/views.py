from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView

from .forms import DonationForm
from .models import Keg, Donation, Purchase

def sum_queryset_field(qs, field):
    return qs.aggregate(Sum(field))[field+'__sum'] or 0

def get_user_balance(user):
    '''Return how many unused votes a user has.'''
    donation_sum = sum_queryset_field(user.donation_set, 'amount')
    spent = sum_queryset_field(user.vote_set, 'value')
    return int(donation_sum - spent)

def fund_context():
    '''total_donations, spent and balance (used on almost every page)'''
    #TODO: This really should be cached
    total_donations = sum_queryset_field(Donation.objects.all(), 'amount')
    spent = sum_queryset_field(Purchase.objects.all(), 'keg__price')
    balance =  total_donations - spent
    return {
        'total_donations': total_donations,
        'spent': spent,
        'balance': balance,
    }

def home(request):
    recent_kegs = Keg.objects.order_by('-added')[:3]
    context = {
        'kegs': recent_kegs,
    }
    context.update(fund_context())
    return render(request, 'index.html', context)

class KegDetail(DetailView):
    model = Keg

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
