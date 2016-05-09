import datetime
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.options import get_content_type_for_model
from django.core.urlresolvers import reverse
from django.db import models
from tinymce.widgets import TinyMCE
from django.utils import timezone

from jobmanager.models import Job, ApplicantType, Grade, JobCategory, Location, JobApplicantType

    
class ApplicantTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("applicant_type",)}
    list_display = ['applicant_type']
    ordering = ['applicant_type']
admin.site.register(ApplicantType,ApplicantTypeAdmin)


class JobApplicantTypeInline(admin.StackedInline):
    model = JobApplicantType
    extra = 1

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

class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
        }
    inlines=[JobApplicantTypeInline,]
    list_display = ['title', 'category', 'close_date']
    search_fields = ('title', 'description')
    list_filter = (JobDatesListFilter,'locations','category','applicant_types',)
    ordering = ['title']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'salary_min',
                'salary_max', 'hourly', 'grades', 'locations', 'open_date',
                'close_date', 'active', 'date_created', 'date_modified')
        }),
        ('Social sharing options', {
            'classes': ('collapse',),
            'description': 'Use these fields to manually specify what title, description, \
                and image should be used on Facebook.',
            'fields': ('open_graph_title', 'open_graph_description', 
                'open_graph_image_url', 'twitter_text', 'utm_campaign')
        }),
    )

    def get_view_on_site_url(self, obj=None):
        if obj is None or not self.view_on_site:
            return None

        if callable(self.view_on_site):
            return self.view_on_site(obj)
        elif self.view_on_site and obj.active and obj.close_date >= timezone.now().date():
            return reverse('admin:view_on_site', kwargs={
                'content_type_id': get_content_type_for_model(obj).pk,
                'object_id': obj.pk
            })
        else:
            return None

admin.site.register(Job, JobAdmin)


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
admin.site.register(JobCategory,JobCategoryAdmin)


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("region_long",)}
    list_display = ['region', 'region_long']
    ordering = ['region']
admin.site.register(Location,LocationAdmin)
