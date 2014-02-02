from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

from .forms import DeletePaymentOptionForm
from .models import PaymentOption


#TODO: Move function create here


@require_POST
@login_required
def delete(request, user_id):
    form = DeletePaymentOptionForm(request.POST)

    if form.is_valid():
        payment = PaymentOption.objects.get(id=form.data['id'])
        # Only delete if it's the same user
        if payment.user == request.user:
            payment.delete()

    return redirect(reverse('main.views.profile', kwargs={'user_id': request.user.id}))