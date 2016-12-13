import datetime
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.options import get_content_type_for_model
from django.core.urlresolvers import reverse
from django.db import models
from tinymce.widgets import TinyMCE
from django.utils import timezone

from jobmanager.models import ApplicantType, Grade, JobCategory, Location


class ApplicantTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("applicant_type",)}
    list_display = ['applicant_type']
    ordering = ['applicant_type']
admin.site.register(ApplicantType, ApplicantTypeAdmin)


class JobDatesListFilter(SimpleListFilter):
    """
    Simplified filter for both start and end dates.
    Options: Open, Past, Future.
    """
    title = ('dates')
    parameter_name = 'dates'

    def lookups(self, request, model_admin):
        return (
                ('past', 'Past'),
                ('open', 'Open'),
                ('future', 'Future')
                )
    def queryset(self, request, queryset):
        today = datetime.date.today()
        if self.value() == 'open':
            return queryset.filter(open_date__lte=today,
                    close_date__gte=today)
        if self.value() == 'past':
            return queryset.filter(close_date__lt=today)
        if self.value() == 'future':
            return queryset.filter(open_date__gt=today)


class GradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("grade",)}
    list_display = ['grade', 'salary_min', 'salary_max']
    ordering = ['-grade']
admin.site.register(Grade,GradeAdmin)


class JobCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("job_category",)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
        }
    list_display = ['job_category']
    ordering = ['job_category']
admin.site.register(JobCategory, JobCategoryAdmin)


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("region_long",)}
    list_display = ['region', 'region_long']
    ordering = ['region']
admin.site.register(Location,LocationAdmin)
