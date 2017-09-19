from django.contrib import admin

from .models import CompanyInfo


def mark_processed(modeladmin, request, queryset):
        queryset.update(processed = True)

mark_processed.short_description = "Mark these records as processed"

def mark_unprocessed(modeladmin, request, queryset):
        queryset.update(processed = False)

mark_unprocessed.short_description = "Mark these records as unprocessed"

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'city', 'state', 'company_phone', 'contact_name', 'contact_phone']
    list_filter = ('processed','state', 'city')
    date_hierarchy = 'submitted'
    actions = [mark_processed, mark_unprocessed]

    def changelist_view(self, request, extra_context=None):

        if not request.GET.has_key('processed__exact'):

            q = request.GET.copy()
            q['processed__exact'] = '0'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(CompanyInfoAdmin,self).changelist_view(request, extra_context=extra_context)

admin.site.register(CompanyInfo, CompanyInfoAdmin)
