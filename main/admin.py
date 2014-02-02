from django.contrib import admin
from .models import Brewery, Keg, KegMaster, UntappdCredentials

admin.site.register(Brewery)
admin.site.register(Keg)
admin.site.register(KegMaster)

# Just in case we need to reset them (there is no identifying info in this)
admin.site.register(UntappdCredentials)