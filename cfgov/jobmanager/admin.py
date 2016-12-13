from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from jobmanager.models import ApplicantType, JobCategory


class ApplicantTypeAdmin(admin.ModelAdmin):
    list_display = ['applicant_type']
    ordering = ['applicant_type']

admin.site.register(ApplicantType, ApplicantTypeAdmin)


class JobCategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    list_display = ['job_category']
    ordering = ['job_category']

admin.site.register(JobCategory, JobCategoryAdmin)
