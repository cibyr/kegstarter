from django.shortcuts import render

from .models import Keg

def home(request):
    recent_kegs = Keg.objects.order_by('-added')[:3]
    context = {'kegs': recent_kegs}
    return render(request, 'index.html', context)
