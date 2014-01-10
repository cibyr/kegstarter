from django.contrib import admin
from .models import Brewery, Keg, KegMaster

admin.site.register(Brewery)
admin.site.register(Keg)
admin.site.register(KegMaster)
