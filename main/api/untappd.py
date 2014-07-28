from django.contrib import messages
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..models import UntappdCredentials, Keg, Brewery
from django.core.urlresolvers import reverse

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import utc

import json

from kegstarter.settings import *
from main.untappd import *

from ..models import UntappdKeg, UntappdBrewery


def init_api(redirect_url=UNTAPPD_REDIRECT_URL, access_token=None):
    """
    @type redirect_url: str
    @type access_token: str
    @rtype: Untappd
    """
    return Untappd(client_id=UNTAPPD_CLIENT_ID,
                   client_secret=UNTAPPD_CLIENT_SECRET,
                   redirect_url=redirect_url,
                   access_token=access_token)


def get_auth_url(untappd_api):
    """
    @type untappd_api: Untappd
    @rtype: str
    """
    return untappd_api.oauth.auth_url()


def get_auth_token(untappd_api, code):
    """
    @type untappd_api: Untappd
    @type code: str
    @rtype: str
    """
    return untappd_api.oauth.get_token(code)


def set_user_token(user, token):
    """
    @type user: User
    @type token: str
    """
    try:
        cred = UntappdCredentials.objects.get(user=user)
    except UntappdCredentials.DoesNotExist:
        cred = UntappdCredentials()
        cred.user = user

    cred.token = token
    # Expires in 5 years (not really even used yet)
    cred.timestamp = datetime.utcnow().replace(tzinfo=utc) + relativedelta(years=5)
    cred.save()


def get_user_token(user):
    """
    @type user: User
    @rtype: UntappdCredentials
    """
    try:
        return UntappdCredentials.objects.get(user=user).token
    except UntappdCredentials.DoesNotExist:
        return None


def expire_user_token(user):
    """
    @type user: User
    """
    try:
        UntappdCredentials.objects.get(user=user).delete()
    except UntappdCredentials.DoesNotExist:
         pass


def search_beer(beer_name, api_v=1):
    """
    @type api_v: int
    @type beer_name: str
    @rtype
    """
    untappd_api = init_api()
    version = int(float(api_v))

    if version == 1:
        response = untappd_api.base_requester.GET(
            path="/search/beer",
            params={
                "q": beer_name
            })

        return response
    else:
        return {}


def get_recent_checkins(untappd_api, api_v=1):
    """
    @type untappd_api: Untappd
    @type api_v: int
    @rtype
    """
    version = int(float(api_v))

    if version == 1:
        response = untappd_api.base_requester.GET(
            path="/user/checkins/",
            params={
                "limit": 10
            })

        return response
    else:
        return {}


def search_beer_view(request, api_v):
    """
    @type request: HttpRequest
    @type api_v: int
    @rtype: HttpResponse
    """
    beer = request.GET.get('beer', None)
    if beer:
        if api_v == u'1':
            response_data = {
                'beer_list': search_beer(beer)
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(status=400, content="You are using an invalid version or missing the version parameter.")


def auth(request):
    """
    @type request: HttpRequest
    @rtype: HttpResponse
    """

    redirect = request.GET.get('r', reverse('home'))
    response = HttpResponseRedirect(redirect)

    # Store our cookie if we authenticated
    if request.GET.get('code', None):
        if request.user:
            untappd_api = init_api()
            token = get_auth_token(untappd_api, request.GET['code'])

            # Set our results
            set_user_token(request.user, token)

            messages.info(request, "Untappd account successfully linked!")
        else:
            messages.error(request, "You must be logged in to link your Untappd account!")

    return response


def create_untappd_keg(bid):
    """
    @type bid: int
    @rtype: UntappdKeg
    """
    if not bid:
        raise UntappdException("Must supply a BID")

    # If we already have the bid in our database, return that instead
    try:
        untappd_keg = UntappdKeg.objects.get(untappd_id=bid)
    except UntappdKeg.DoesNotExist:
        untappd_keg = UntappdKeg()
        untappd_keg.expires = UntappdKeg.get_default_expiry()
        untappd_keg.untappd_id = bid
        untappd_keg.untappd_brewery = create_untappd_brewery(get_kegs_brewery_id(bid))
        untappd_keg.save()

    return untappd_keg


def get_kegs_brewery_id(bid, untappd_api=init_api()):
    beer = untappd_api.Beer(untappd_api.base_requester)
    beer_info = beer.GET(path=("info/{}".format(bid)))

    return beer_info['beer']['brewery']['brewery_id']


def create_untappd_brewery(brid):
    """
    @type brid: int
    @rtype: UntappdBrewery
    """

    # If we already have the brid in our database, return that instead
    try:
        untappd_brewery = UntappdBrewery.objects.get(untappd_id=brid)
    except UntappdBrewery.DoesNotExist:
        untappd_brewery = UntappdBrewery()
        untappd_brewery.expires = UntappdKeg.get_default_expiry()
        untappd_brewery.untappd_id = brid
        untappd_brewery.save()

    return untappd_brewery


def cache_brewery(untappd_brewery, untappd_api=init_api()):
    """
        @type untappd_api: Untappd
        @type untappd_brewery: UntappdBrewery
    """
    if not untappd_api:
        raise UntappdException("Must supply an Untappd API Object")
    if not untappd_brewery:
        raise UntappdException("Must supply an Untappd Brewery Model")

    brew = untappd_api.Brewery(untappd_api.base_requester)
    brew_info = brew.GET(path=("info/{}".format(untappd_brewery.untappd_id)))

    brewery = Brewery()
    brewery.name = brew_info['brewery']['brewery_name']
    location = brew_info['brewery']['location']
    if not location['brewery_state']:
        brewery.location = u"{} ({})".format(
            location['brewery_address'],
            location['brewery_city'])
    else:
        brewery.location = u"{} ({}, {})".format(
            location['brewery_address'],
            location['brewery_city'],
            location['brewery_state'])
    brewery.desc = brew_info['brewery']['brewery_description']
    brewery.image = brew_info['brewery']['brewery_label']
    brewery.save()

    return brewery


def cache_keg(untappd_keg, untappd_api=init_api()):
    """
        @type untappd_api: Untappd
        @type untappd_keg: UntappdKeg
    """
    if not untappd_api:
        raise UntappdException("Must supply an Untappd API Object")
    if not untappd_keg:
        raise UntappdException("Must supply an Untappd Keg Model")

    beer = untappd_api.Beer(untappd_api.base_requester)
    beer_info = beer.GET(path=("info/{}".format(untappd_keg.untappd_id)))

    keg = Keg()
    keg.name = beer_info['beer']['beer_name']
    keg.style = beer_info['beer']['beer_style']
    keg.desc = beer_info['beer']['beer_description']
    keg.image = beer_info['beer']['beer_label']
    keg.rating = beer_info['beer']['rating_score']
    keg.save()

    return keg
