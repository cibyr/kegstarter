from django.contrib import admin
from .models import Brewery, Keg, KegMaster, Suggestion, UntappdCredentials, Purchase

admin.site.register(Brewery)
admin.site.register(Keg)
admin.site.register(KegMaster)
admin.site.register(Suggestion)
admin.site.register(Purchase)

# Just in case we need to reset them (there is no identifying info in this)
admin.site.register(UntappdCredentials)
