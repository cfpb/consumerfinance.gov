from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from jobmanager.models import ApplicantType, JobListingPage


class ApplicantTypeModelAdmin(ModelAdmin):
    model = ApplicantType
    menu_label = 'Applicant types'
    menu_icon = 'snippet'


class JobListingModelAdmin(ModelAdmin):
    model = JobListingPage
    menu_label = 'Job listing pages'
    menu_icon = 'doc-full-inverse'


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Job listings'
    menu_icon = 'folder-open-inverse'
    items = (ApplicantTypeModelAdmin, JobListingModelAdmin,)
