from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Sum, Max, Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView

from datetime import datetime
from re import match

from .forms import DonationForm, VoteForm, PurchaseForm, KegForm, PurchasePriceForm, AddPaymentOptionForm
from .models import Brewery, Donation, Purchase, KegMaster, PaymentOption, Suggestion
from .shared import sum_queryset_field, get_user_balance

from main.api.untappd import *

def get_current_kegmaster():
    '''Return the latest Keg Master that hasn't ended their shift'''
    now = datetime.utcnow().replace(tzinfo=utc)
    kegmasters = KegMaster.objects.filter(start__lte=now)
    kegmasters = kegmasters.filter(Q(end__gte=now) | Q(end__isnull=True))
    latest_kegmaster = kegmasters.order_by('end')
    if latest_kegmaster:
        return latest_kegmaster[0]


def get_user_payment_options(user, preferred=False):
    users_payment_options = PaymentOption.objects.filter(user=user)
    if preferred:
        users_payment_options = users_payment_options.filter(preferred=True)
    return users_payment_options.order_by('preferred').reverse()

def fund_context():
    '''total_donations, spent and balance (used on almost every page)'''
    #TODO: This really should be cached
    total_donations = sum_queryset_field(Donation.objects.all(), 'amount')
    spent = sum_queryset_field(Purchase.objects.all(), 'suggestion__price')
    balance =  total_donations - spent
    return {
        'total_donations': total_donations,
        'spent': spent,
        'balance': balance,
    }

def home(request):
    not_purchased = Suggestion.objects.filter(purchase=None)
    recent_suggestions = not_purchased.order_by('-timestamp')[:3]
    winning_suggestions = not_purchased.annotate(votes_sum=Sum('vote__value')).order_by('-votes_sum')
    keg_master = get_current_kegmaster()
    if keg_master is None:
        payment_options = None
    else:
        payment_options = get_user_payment_options(keg_master.user, preferred=True)
        # Simple regex to censor any emails on the front page since you don't need to be
        # logged in to view.  This will help our users from bots scraping for emails.
        for payment in payment_options:
            if match(r"[^@]+@[^@]+\.[^@]+", payment.value):
                payment.value = "Email Address Censored"
                payment.info = "Go to user's account to view"
    context = {
        'suggestions': recent_suggestions,
        'winning_suggestions': winning_suggestions,
        'current_kegmaster': keg_master,
        'current_kegmaster_payment_options': payment_options,
        'purchase_history': get_keg_purchase_history()
    }
    context.update(fund_context())
    response = render(request, 'index.html', context)

    return response

def get_winning_suggestions(current_balance):
    buyable_suggestions = Suggestion.objects.filter(price__lte=current_balance)
    nonpurchased_suggestions = buyable_suggestions.filter(purchase=None)
    suggestions_by_votes = nonpurchased_suggestions.annotate(votes=Sum('vote__value'))
    max_votes = suggestions_by_votes.aggregate(Max('votes'))['votes__max']
    return suggestions_by_votes.filter(votes=max_votes)

class KegDetail(DetailView):
    model = Suggestion

    def get_context_data(self, **kwargs):
        context = super(KegDetail, self).get_context_data(**kwargs)
        context.update(fund_context())
        winning_suggestions = get_winning_suggestions(context['balance'])
        if self.request.user.is_authenticated():
            current_kegmaster = get_current_kegmaster()
            if current_kegmaster:
                context['user_is_current_kegmaster'] = (self.request.user == current_kegmaster.user)
            else:
                context['user_is_current_kegmaster'] = False
            context['user_balance'] = get_user_balance(self.request.user)
            context['winning'] = (self.object in winning_suggestions)
            context['purchaseprice_form'] = PurchasePriceForm(instance=self.object)
            context['purchase_form'] = PurchaseForm(initial={'suggestion': self.object})
        return context


@login_required
def create_keg(request):
    context = {}

    if request.method == 'POST':
        bid = request.POST.get('bid', None)
        if bid:
            untappd_keg = create_untappd_keg(bid)

            suggestion = Suggestion()
            suggestion.untappd_keg = untappd_keg
            suggestion.proposed_by = request.user
            suggestion.price = 0
            suggestion.gallons = 15.5
            suggestion.save()

            return HttpResponseRedirect(suggestion.get_absolute_url())

        return HttpResponseRedirect(reverse('keg_create'))
    else:
        form = KegForm()

        token = get_user_token(request.user)
        untappd_api = init_api(redirect_url=UNTAPPD_REDIRECT_URL, access_token=token)

        context['untappd_has_token'] = (token is not None)
        if token is None:
            context['untappd_auth_url'] = get_auth_url(untappd_api)
        else:
            context['recent_checkins'] = get_recent_checkins(untappd_api)

        beer = request.GET.get('beer', None)
        if beer:
            context['search'] = beer
            context['search_results'] = search_beer(beer)

    context['form'] = form
    return render(request, 'main/keg_form.html', context)


@login_required
def profile(request, user_id):
    try:
        requested_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        requested_user = request.user

    context = {
        'payment_options': get_user_payment_options(requested_user),
        'requested_user': requested_user
    }

    # Only display form is it's same user
    if requested_user == request.user:
        context['same_user'] = True
        if request.method == 'POST':
            form = AddPaymentOptionForm(request.POST)

            if form.is_valid():
                payment_option = form.save(commit=False)
                payment_option.user = request.user
                payment_option.save()
                form = AddPaymentOptionForm()
        else:
            form = AddPaymentOptionForm()

        context['payment_options_form'] = form

    return render(request, 'main/profile.html', context)

class BreweryDetail(DetailView):
    model = UntappdBrewery

    def get_context_data(self, **kwargs):
        context = super(BreweryDetail, self).get_context_data(**kwargs)

        context['untappd_kegs'] = UntappdKeg.objects.filter(untappd_brewery__exact=context['object'])
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
                vote.value, 's' if vote.value > 1 else '', vote.suggestion.untappd_keg))
        return HttpResponseRedirect(vote.suggestion.get_absolute_url())
    else:
        return HttpResponseBadRequest()


@require_POST
@login_required
def purchase(request):
    form = PurchaseForm(request.POST)
    form_kegprice = PurchasePriceForm(request.POST)
    if form.is_valid() and form_kegprice.is_valid():
        purchase = form.save(commit=False)
        kegprice = form_kegprice.save(commit=False)
        purchase.suggestion.price = kegprice.price
        # Check that the keg is the current winner
        current_balance = fund_context()['balance']
        if purchase.suggestion not in get_winning_suggestions(current_balance):
            return HttpResponseBadRequest('Not the winning keg')
        # Check that the user is the current kegmaster
        if request.user != get_current_kegmaster().user:
            return HttpResponseBadRequest('You are not kegmaster')
        purchase.user = request.user
        #TODO: take a lock on something (the user?) to prevent a double-purchase
        # in a race here
        purchase.save()
        purchase.suggestion.save()
        messages.info(request, "Purchase of {} successfully recorded".format(purchase.suggestion.untappd_keg))
        return HttpResponseRedirect(purchase.suggestion.get_absolute_url())
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
    context = {
        'form': form,
        'new_donation': new_donation,
        'donation_history': get_donation_history(request.user)
    }
    return render(request, 'donation.html', context)

def get_donation_history(user):
    return Donation.objects.filter(recipient__exact=user).order_by('timestamp')

def get_keg_purchase_history():
    return Purchase.objects.order_by('-timestamp')
