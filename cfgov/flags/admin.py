from django.contrib import admin

from flags.models import Flag, FlagState

admin.site.register(Flag)
admin.site.register(FlagState)
