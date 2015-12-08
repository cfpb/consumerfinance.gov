from django.contrib import admin
from models.snippets import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

