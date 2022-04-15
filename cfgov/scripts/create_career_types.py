import json

from jobmanager.models import (
    ApplicantType,
    JobLength,
    JobListingPage,
    ServiceType,
)


APPLICANT_TYPES = [
    {
        "title": "Open to the public",
        "description": "U.S. citizens, nationals, or those who owe "
        "allegiance to the U.S., and excepted service "
        "employees are invited to apply for this position.",
        "related_term": "Open to All US Citizens",
    },
    {
        "title": "Status candidates",
        "description": "Federal employees, including current and former "
        "competitive service, veterans, and individuals "
        "with a disability, are invited to apply for "
        "this position.",
        "related_term": "Open to status candidates",
    },
]

JOB_LENGTHS = ["Permanent", "Term to perm", "Term", "Temporary"]

SERVICE_TYPES = ["Competitive service", "Excepted service"]


applicant_type_dict = {}
job_length_dict = {}
service_type_dict = {}


def create_new_types():
    for a in APPLICANT_TYPES:
        new_type, cr = ApplicantType.objects.update_or_create(
            applicant_type=a["title"], description=a["description"]
        )
        applicant_type_dict[a["related_term"]] = new_type
    for j in JOB_LENGTHS:
        new_type, cr = JobLength.objects.update_or_create(job_length=j)
        job_length_dict[j.lower()] = new_type
    for s in SERVICE_TYPES:
        new_type, cr = ServiceType.objects.update_or_create(service_type=s)
        service_type_dict[s.lower()] = new_type


def update_job_pages():
    if not JobListingPage.objects.exists():
        return

    job_lengths = job_length_dict.keys()
    service_types = service_type_dict.keys()
    new_applicant_types = applicant_type_dict.keys()

    for page in JobListingPage.objects.all():
        for link in page.usajobs_application_links.all():
            if link.applicant_type and link.applicant_type.applicant_type:
                current_applicant_type = (
                    link.applicant_type.applicant_type.lower()
                )
                for a in new_applicant_types:
                    if a.lower() in current_applicant_type:
                        link.applicant_type = applicant_type_dict[a]
                for s in service_types:
                    if s in current_applicant_type:
                        page.service_type = service_type_dict[s]
                for j in job_lengths:
                    if j in current_applicant_type:
                        page.job_length = job_length_dict[j]

                link.save()
                page.save()

        for revision in page.revisions.all():
            content = json.loads(revision.content_json)
            usajobs_application_links = content["usajobs_application_links"]

            for link in usajobs_application_links:
                applicant_type = ApplicantType.objects.filter(
                    pk=link["applicant_type"]
                ).first()
                if applicant_type and applicant_type.applicant_type:
                    current_applicant_type = (
                        applicant_type.applicant_type.lower()
                    )
                    for s in service_types:
                        if s in current_applicant_type:
                            content["service_type"] = service_type_dict[s].pk
                    for j in job_lengths:
                        if j in current_applicant_type:
                            content["job_length"] = job_length_dict[j].pk
                    for a in new_applicant_types:
                        if a.lower() in current_applicant_type:
                            link["applicant_type"] = applicant_type_dict[a].pk
        revision.content_json = json.dumps(content)
        revision.save()


def remove_old_applicant_types():
    for type_string in applicant_type_dict.keys():
        old_applicant_types = ApplicantType.objects.filter(
            applicant_type__icontains=type_string
        )
        for applicant_type in old_applicant_types:
            applicant_type.delete()


def add_display_titles():
    cfpb_employee_types = ApplicantType.objects.filter(
        applicant_type__icontains="Open to CFPB employees only"
    )
    for applicant_type in cfpb_employee_types:
        applicant_type.display_title = "Open to CFPB employees only"
        applicant_type.save()


def run():
    create_new_types()
    update_job_pages()
    remove_old_applicant_types()
    add_display_titles()
