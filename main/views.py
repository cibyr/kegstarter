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


from .forms import DonationForm, VoteForm, PurchaseForm, BreweryForm, KegForm, PurchasePriceForm, AddPaymentOptionForm
from .models import Brewery, Keg, Donation, Purchase, KegMaster, PaymentOption

def get_current_kegmaster():
    '''Return the latest Keg Master that hasn't ended their shift'''
    now = datetime.utcnow().replace(tzinfo=utc)
    kegmasters = KegMaster.objects.filter(start__lte=now)
    kegmasters = kegmasters.filter(Q(end__gte=now) | Q(end__isnull=True))
    latest_kegmaster = kegmasters.order_by('end')
    if latest_kegmaster:
        return latest_kegmaster[0]

def sum_queryset_field(qs, field):
    return qs.aggregate(Sum(field))[field+'__sum'] or 0

def get_user_balance(user):
    '''Return how many unused votes a user has.'''
    donation_sum = sum_queryset_field(user.donation_set, 'amount')
    spent = sum_queryset_field(user.vote_set, 'value')
    return int(donation_sum - spent)


def get_user_payment_options(user, preferred=False):
    users_payment_options = PaymentOption.objects.filter(user=user)
    if preferred:
        users_payment_options = users_payment_options.filter(preferred=True)
    return users_payment_options.order_by('preferred').reverse()

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
    not_purchased = Keg.objects.filter(purchase=None)
    recent_kegs = not_purchased.order_by('-added')[:3]
    winning_kegs = not_purchased.annotate(votes_sum=Sum('vote__value')).order_by('-votes_sum')
    keg_master = get_current_kegmaster()
    context = {
        'kegs': recent_kegs,
        'winning_kegs': winning_kegs,
        'current_kegmaster': keg_master,
        'current_kegmaster_payment_options': get_user_payment_options(keg_master, preferred=True),
        'purchase_history': get_keg_purchase_history()
    }
    context.update(fund_context())
    return render(request, 'index.html', context)

def get_winning_kegs(current_balance):
    buyable_kegs = Keg.objects.filter(price__lte=current_balance)
    nonpurchased_kegs = buyable_kegs.filter(purchase=None)
    kegs_by_votes = nonpurchased_kegs.annotate(votes=Sum('vote__value'))
    max_votes = kegs_by_votes.aggregate(Max('votes'))['votes__max']
    return kegs_by_votes.filter(votes=max_votes)

class KegDetail(DetailView):
    model = Keg

    def get_context_data(self, **kwargs):
        context = super(KegDetail, self).get_context_data(**kwargs)
        context.update(fund_context())
        winning_kegs = get_winning_kegs(context['balance'])
        if self.request.user.is_authenticated():
            current_kegmaster = get_current_kegmaster()
            if current_kegmaster:
                context['user_is_current_kegmaster'] = (self.request.user == current_kegmaster.user)
            else:
                context['user_is_current_kegmaster'] = False
            context['user_balance'] = get_user_balance(self.request.user)
            context['winning'] = (self.object in winning_kegs)
            context['purchaseprice_form'] = PurchasePriceForm(instance=self.object)
            context['purchase_form'] = PurchaseForm(initial={'keg': self.object})
        return context


@login_required
def create_keg(request):
    if request.method == 'POST':
        form = KegForm(request.POST)
        if form.is_valid():
            keg = form.save(commit=False)
            keg.proposed_by = request.user
            keg.save()
            return HttpResponseRedirect(keg.get_absolute_url())
    else:
        form = KegForm()

    return render(request, 'main/keg_form.html', {'form': form})


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
    if requested_user.id is request.user.id:
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
    model = Brewery


@login_required
def create_brewery(request):
    if request.method == 'POST':
        form = BreweryForm(request.POST)
        if form.is_valid():
            brewery = form.save(commit=False)
            brewery.added_by = request.user
            brewery.save()
            return HttpResponseRedirect(brewery.get_absolute_url())
    else:
        form = BreweryForm()

    return render(request, 'main/brewery_form.html', {'form': form})


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


@require_POST
@login_required
def purchase(request):
    form = PurchaseForm(request.POST)
    form_kegprice = PurchasePriceForm(request.POST)
    if form.is_valid() and form_kegprice.is_valid():
        purchase = form.save(commit=False)
        kegprice = form_kegprice.save(commit=False)
        purchase.keg.price = kegprice.price
        # Check that the keg is the current winner
        current_balance = fund_context()['balance']
        if purchase.keg not in get_winning_kegs(current_balance):
            return HttpResponseBadRequest('Not the winning keg')
        # Check that the user is the current kegmaster
        if request.user != get_current_kegmaster().user:
            return HttpResponseBadRequest('You are not kegmaster')
        purchase.user = request.user
        #TODO: take a lock on something (the user?) to prevent a double-purchase
        # in a race here
        purchase.save()
        purchase.keg.save()
        messages.info(request, "Purchase of {} sucessfully recorded".format(purchase.keg))
        return HttpResponseRedirect(purchase.keg.get_absolute_url())
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
    return Purchase.objects.order_by('timestamp')
