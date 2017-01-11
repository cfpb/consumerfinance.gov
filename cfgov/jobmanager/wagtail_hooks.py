from django.forms.models import ModelForm
from tinymce.widgets import TinyMCE
from wagtail.contrib.modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                modeladmin_register)
from wagtail.contrib.modeladmin.views import CreateView, EditView, InspectView

from jobmanager.models import (ApplicantType, Grade, JobCategory,
                               JobListingPage, JobRegion)


class ApplicantTypeModelAdmin(ModelAdmin):
    model = ApplicantType
    menu_label = 'Applicant types'
    menu_icon = 'snippet'


class JobGradeModelAdmin(ModelAdmin):
    model = Grade
    menu_label = 'Grades'
    menu_icon = 'snippet'
    list_display = ('grade', 'salary_min', 'salary_max')


class JobCategoryForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = JobCategory
        widgets = {
            'blurb': TinyMCE(attrs={'cols': 80, 'rows': 15}),
        }


class JobCategoryModelFormMixin(object):
    def get_form_class(self):
        return JobCategoryForm


class JobCategoryCreateView(JobCategoryModelFormMixin, CreateView):
    pass


class JobCategoryEditView(JobCategoryModelFormMixin, EditView):
    pass


class JobCategoryInspectView(JobCategoryModelFormMixin, InspectView):
    pass


class JobCategoryModelAdmin(ModelAdmin):
    model = JobCategory
    menu_label = 'Divisions'
    menu_icon = 'snippet'
    create_view_class = JobCategoryCreateView
    edit_view_class = JobCategoryEditView
    inspect_view_class = JobCategoryInspectView


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
    model = JobRegion
    menu_label = 'Regions'
    menu_icon = 'site'
    list_display = ('abbreviation', 'name')


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Job listings'
    menu_icon = 'folder-open-inverse'
    items = (
        ApplicantTypeModelAdmin,
        JobCategoryModelAdmin,
        JobGradeModelAdmin,
        JobRegionModelAdmin,
    )
