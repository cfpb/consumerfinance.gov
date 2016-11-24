from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from jobmanager.models import (
    ApplicantType, Grade, JobCategory, JobListingPage, Location
)


class ApplicantTypeModelAdmin(ModelAdmin):
    model = ApplicantType
    menu_label = 'Applicant types'
    menu_icon = 'snippet'


class JobGradeModelAdmin(ModelAdmin):
    model = Grade
    menu_label = 'Grades'
    menu_icon = 'snippet'
    list_display = ('grade', 'salary_min', 'salary_max')


class JobCategoryModelAdmin(ModelAdmin):
    model = JobCategory
    menu_label = 'Divisions'
    menu_icon = 'snippet'


class JobListingModelAdmin(ModelAdmin):
    model = JobListingPage
    menu_label = 'Job listing pages'
    menu_icon = 'doc-full-inverse'
    list_display = (
        'title', 'division', 'grades', 'regions', 'open_date', 'close_date'
    )
    search_fields = ('title',)

    def grades(self, page):
        return ', '.join(page.ordered_grades)

    def regions(self, page):
        return ', '.join(page.ordered_regions)


class JobRegionModelAdmin(ModelAdmin):
    model = Location
    menu_label = 'Regions'
    menu_icon = 'snippet'
    list_display = ('description', 'region', 'region_long')


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Job listings'
    menu_icon = 'folder-open-inverse'
    items = (
        ApplicantTypeModelAdmin,
        JobCategoryModelAdmin,
        JobGradeModelAdmin,
        JobListingModelAdmin,
        JobRegionModelAdmin,
    )
