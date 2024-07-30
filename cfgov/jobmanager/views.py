from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from jobmanager.models import (
    ApplicantType,
    Grade,
    JobCategory,
    JobLength,
    Office,
    Region,
    ServiceType,
)


class ApplicantTypeViewSet(SnippetViewSet):
    model = ApplicantType
    icon = "snippet"
    menu_label = "Applicant types"


class GradeViewSet(SnippetViewSet):
    model = Grade
    icon = "snippet"
    menu_label = "Grades"
    list_display = ["grade", "salary_min", "salary_max"]


class JobCategoryViewSet(SnippetViewSet):
    model = JobCategory
    icon = "snippet"
    menu_label = "Divisions"


class JobLengthViewSet(SnippetViewSet):
    model = JobLength
    icon = "site"
    menu_label = "Job Length"


class OfficeViewSet(SnippetViewSet):
    model = Office
    icon = "site"
    menu_label = "Offices"
    list_display = ["abbreviation", "__str__"]


class RegionViewSet(SnippetViewSet):
    model = Region
    icon = "site"
    menu_label = "Regions"

    list_display = [
        "abbreviation",
        "name",
        "states_in_region",
        "major_city_names",
    ]


class ServiceTypeViewSet(SnippetViewSet):
    model = ServiceType
    icon = "site"
    menu_label = "Service Type"


class JobListingsViewSetGroup(SnippetViewSetGroup):
    items = [
        ApplicantTypeViewSet,
        GradeViewSet,
        JobCategoryViewSet,
        JobLengthViewSet,
        OfficeViewSet,
        RegionViewSet,
        ServiceTypeViewSet,
    ]
    menu_label = "Job listings"
    menu_icon = "folder-open-inverse"
