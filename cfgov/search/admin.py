from django.contrib import admin

from search.models import Synonym


class SynonymAdmin(admin.ModelAdmin):
    list_display = ("synonym", )
    search_fields = ("synonym", )
    ordering = ("synonym", )


admin.site.register(Synonym, SynonymAdmin)
