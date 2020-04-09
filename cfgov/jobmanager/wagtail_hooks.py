from django.conf.urls import include, url
from django.forms.models import ModelForm

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from wagtail.contrib.modeladmin.views import CreateView, EditView, InspectView
from wagtail.core import hooks

from jobmanager import template_debug
from jobmanager.models import (
    ApplicantType, Grade, JobCategory, JobLength, Office, Region, ServiceType
)
from v1.views.template_debug import TemplateDebugView


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


class JobRegionModelAdmin(ModelAdmin):
    model = Region
    menu_label = 'Regions'
    menu_icon = 'site'

    def states_in_region(self):
        return ", ".join(str(state) for state in self.states.all())

    def major_cities(self):
        return "; ".join(str(city) for city in self.major_cities.all())

    list_display = ('abbreviation', 'name', states_in_region, major_cities)


class JobOfficeModelAdmin(ModelAdmin):
    model = Office
    menu_label = 'Offices'
    menu_icon = 'site'
    list_display = ('abbreviation', '__str__')


class ServiceTypeModelAdmin(ModelAdmin):
    model = ServiceType
    menu_label = 'Service Type'
    menu_icon = 'site'


class JobLengthModelAdmin(ModelAdmin):
    model = JobLength
    menu_label = 'Job Length'
    menu_icon = 'site'


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Job listings'
    menu_icon = 'folder-open-inverse'
    items = (
        ApplicantTypeModelAdmin,
        JobCategoryModelAdmin,
        JobGradeModelAdmin,
        ServiceTypeModelAdmin,
        JobLengthModelAdmin,
        JobOfficeModelAdmin,
        JobRegionModelAdmin
    )


@hooks.register('register_admin_urls')
def register_admin_urls():
    urls = [
        url(
            rf'^template_debug/jobmanager/{template_name}/',
            TemplateDebugView.as_view(
                debug_template_name=f'jobmanager/{template_name}.html',
                debug_test_cases=getattr(
                    template_debug,
                    f'{template_name}_test_cases'
                )
            ),
            name=f'template_debug_{template_name}'
        ) for template_name in (
            'job_listing_details',
            'job_listing_json_ld',
            'job_listing_list',
            'job_listing_table',
        )
    ]

    return [
        url('', include(urls, namespace='jobmanager')),
    ]
