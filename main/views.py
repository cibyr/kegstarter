from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from .forms import DonationForm, VoteForm
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

    def get_context_data(self, **kwargs):
        context = super(KegDetail, self).get_context_data(**kwargs)
        context.update(fund_context())
        if self.request.user.is_authenticated():
            context['user_balance'] = get_user_balance(self.request.user)
        context['votes'] = sum_queryset_field(self.object.vote_set, 'value')
        return context

@require_POST
@login_required
def vote(request):
    form = VoteForm(request.POST)
    if form.is_valid() and form.cleaned_data['value'] > 0:
        vote = form.save(commit=False)
        vote.user = request.user
        #TODO: take a lock on something (the user?) to prevent a user being able
        # to "overspend" their votes in a race here
        if vote.value > get_user_balance(request.user):
            messages.error("Vote failed: you don't have that many votes")
        else:
            vote.save()
            messages.info(request, "{} vote{} for {} sucessfully recorded".format(
                vote.value, 's' if vote.value > 1 else '', vote.keg))
        return HttpResponseRedirect(vote.keg.get_absolute_url())
    else:
        return HttpResponseBadRequest()

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
