from django.forms.models import ModelForm

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.contrib.modeladmin.views import CreateView, EditView, InspectView

from jobmanager import template_debug
from jobmanager.models import (
    ApplicantType,
    Grade,
    JobCategory,
    JobLength,
    Office,
    Region,
    ServiceType,
)
from v1.template_debug import register_template_debug


class ApplicantTypeModelAdmin(ModelAdmin):
    model = ApplicantType
    menu_label = "Applicant types"
    menu_icon = "snippet"


class JobGradeModelAdmin(ModelAdmin):
    model = Grade
    menu_label = "Grades"
    menu_icon = "snippet"
    list_display = ("grade", "salary_min", "salary_max")


class JobCategoryForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = JobCategory


class JobCategoryModelFormMixin:
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
    menu_label = "Divisions"
    menu_icon = "snippet"
    create_view_class = JobCategoryCreateView
    edit_view_class = JobCategoryEditView
    inspect_view_class = JobCategoryInspectView


class JobRegionModelAdmin(ModelAdmin):
    model = Region
    menu_label = "Regions"
    menu_icon = "site"

    def states_in_region(self):
        return ", ".join(str(state) for state in self.states.all())

    def major_cities(self):
        return "; ".join(str(city) for city in self.major_cities.all())

    list_display = ("abbreviation", "name", states_in_region, major_cities)


class JobOfficeModelAdmin(ModelAdmin):
    model = Office
    menu_label = "Offices"
    menu_icon = "site"
    list_display = ("abbreviation", "__str__")


class ServiceTypeModelAdmin(ModelAdmin):
    model = ServiceType
    menu_label = "Service Type"
    menu_icon = "site"


class JobLengthModelAdmin(ModelAdmin):
    model = JobLength
    menu_label = "Job Length"
    menu_icon = "site"


@modeladmin_register
class MyModelAdminGroup(ModelAdminGroup):
    menu_label = "Job listings"
    menu_icon = "folder-open-inverse"
    items = (
        ApplicantTypeModelAdmin,
        JobCategoryModelAdmin,
        JobGradeModelAdmin,
        ServiceTypeModelAdmin,
        JobLengthModelAdmin,
        JobOfficeModelAdmin,
        JobRegionModelAdmin,
    )


for _debug_template_name in (
    "job_listing_details",
    "job_listing_list",
    "job_listing_table",
):
    register_template_debug(
        "jobmanager",
        _debug_template_name,
        f"jobmanager/{_debug_template_name}.html",
        getattr(template_debug, f"{_debug_template_name}_test_cases"),
    )
