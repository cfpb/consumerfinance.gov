"""
Utilities for querying the Dept of Ed's College Scorecard API.

The API, released 2015-09-12, requires a key, which you can get
from https://api.data.gov/signup/
- API repo:
    https://github.com/18F/open-data-maker
- collegechoice repo:
    https://github.com/18F/college-choice
- raw data:
    https://s3.amazonaws.com/ed-college-choice-public/CollegeScorecard_Raw_Data.zip
- api_key usage:
    https://api.data.gov/docs/api-key/
"""
import os

import requests


API_KEY = os.getenv("ED_API_KEY", "")
API_ROOT = "https://api.data.gov/ed/collegescorecard/v1"
SCHOOLS_ROOT = "{}/schools.json".format(API_ROOT)
QUERY_URL = "{}?id={}&api_key={}&fields={}"
PAGE_MAX = 100  # the max page size allowed as of 2015-09-14

MODEL_MAP = {
    "ope6_id": "ope6_id",
    "ope8_id": "ope8_id",
    "school.accreditor": "accreditor",
    "school.school_url": "url",
    "school.city": "city",
    "school.state": "state",
    "school.degrees_awarded.predominant": "degrees_predominant",
    "school.degrees_awarded.highest": "degrees_highest",
    "school.ownership": "ownership",
    "school.main_campus": "main_campus",
    "school.online_only": "online_only",
    "school.operating": "operating",
    "school.under_investigation": "under_investigation",
    "school.zip": "zip5",
    "latest.cost.tuition.out_of_state": "tuition_out_of_state",
    "latest.cost.tuition.in_state": "tuition_in_state",
    "latest.earnings.10_yrs_after_entry.median": "median_annual_pay",
    "latest.earnings.6_yrs_after_entry.median": "median_annual_pay_6yr",
    "latest.student.size": "enrollment",
}

# decimal values must be converted to Python Decimal before insertion
# two decimal values, grad_rate_4yr and grad_rate_lt4, are processed separately
DECIMAL_MAP = {
    "latest.aid.median_debt_suppressed.overall": "median_total_debt",
    "latest.aid.median_debt_suppressed.completers.monthly_payments": "median_monthly_debt",  # noqa
    "latest.completion.transfer_rate.less_than_4yr.full_time": "associate_transfer_rate",  # noqa
    "latest.repayment.repayment_cohort.3_year_declining_balance": "repay_3yr",
    "latest.repayment.repayment_cohort.5_year_declining_balance": "repay_5yr",
    "latest.repayment.5_yr_default_rate": "default_rate",
}

# scorecard program categories, with API slug and full-name, obtained from:
# https://raw.githubusercontent.com/RTICWDT/college-scorecard/dev/_data/programs.csv. # noqa
PROGRAM_CATEGORIES = {
    "agriculture": "Agriculture, Agriculture Operations, and Related Sciences",
    "architecture": "Architecture and Related Services",
    "ethnic_cultural_gender": "Area, Ethnic, Cultural, Gender, and Group Studies",  # noqa
    "biological": "Biological and Biomedical Sciences",
    "business_marketing": "Business, Management, Marketing, and Related Support Services",  # noqa
    "communication": "Communication, Journalism, and Related Programs",
    "communications_technology": "Communications Technologies/Technicians and Support Services",  # noqa
    "computer": "Computer and Information Sciences and Support Services",
    "construction": "Construction Trades",
    "education": "Education",
    "engineering": "Engineering",
    "engineering_technology": "Engineering Technologies and Engineering-Related Fields",  # noqa
    "english": "English Language and Literature/Letters",
    "family_consumer_science": "Family and Consumer Sciences/Human Sciences",
    "language": "Foreign Languages, Literatures, and Linguistics",
    "health": "Health Professions and Related Programs",
    "history": "History",
    "security_law_enforcement": "Homeland Security, Law Enforcement, Firefighting and Related Protective Services",  # noqa
    "legal": "Legal Professions and Studies",
    "humanities": "Liberal Arts and Sciences, General Studies and Humanities",
    "library": "Library Science",
    "mathematics": "Mathematics and Statistics",
    "mechanic_repair_technology": "Mechanic and Repair Technologies/Technicians",  # noqa
    "military": "Military Technologies and Applied Sciences",
    "multidiscipline": "Multi/Interdisciplinary Studies",
    "resources": "Natural Resources and Conservation",
    "parks_recreation_fitness": "Parks, Recreation, Leisure, and Fitness Studies",  # noqa
    "personal_culinary": "Personal and Culinary Services",
    "philosophy_religious": "Philosophy and Religious Studies",
    "physical_science": "Physical Sciences",
    "precision_production": "Precision Production",
    "psychology": "Psychology",
    "public_administration_social_service": "Public Administration and Social Service Professions",  # noqa
    "science_technology": "Science Technologies/Technicians",
    "social_science": "Social Sciences",
    "theology_religious_vocation": "Theology and Religious Vocations",
    "transportation": "Transportation and Materials Moving",
    "visual_performing": "Visual and Performing Arts",
}


def assemble_program_fields():
    """Generate the API fields needed to compile school program info."""
    field_string = "academics.program_percentage.{}"
    return [field_string.format(category) for category in PROGRAM_CATEGORIES]


BASE_FIELDS = [
    "id",
    "ope6_id",
    "school.name",
    "school.city",
    "school.state",
    "school.zip",
    "school.accreditor",
    "school.school_url",
    "school.degrees_awarded.predominant",
    "school.degrees_awarded.highest",
    "school.ownership",
    "school.main_campus",
    "school.branches",
    "school.online_only",
    "school.operating",
    "school.under_investigation",
]


YEAR_FIELDS = assemble_program_fields() + [
    "admissions.admission_rate.overall",
    "admissions.admission_rate.by_ope_id",
    "aid.federal_loan_rate",
    "aid.cumulative_debt.number",
    "aid.cumulative_debt.90th_percentile",
    "aid.cumulative_debt.75th_percentile",
    "aid.cumulative_debt.25th_percentile",
    "aid.cumulative_debt.10th_percentile",
    "aid.median_debt_suppressed.overall",
    "aid.median_debt_suppressed.completers.overall",
    "aid.median_debt_suppressed.completers.monthly_payments",
    "aid.students_with_any_loan",
    "completion.completion_rate_4yr_150nt_pooled",
    "completion.completion_rate_less_than_4yr_150nt_pooled",
    "cost.attendance.academic_year",
    "cost.attendance.program_year",
    "cost.tuition.in_state",
    "cost.tuition.out_of_state",
    "cost.tuition.program_year",
    "cost.avg_net_price.private",
    "cost.net_price.private.by_income_level.0-30000",
    "cost.net_price.private.by_income_level.30001-48000",
    "cost.net_price.private.by_income_level.48001-75000",
    "cost.net_price.private.by_income_level.75001-110000",
    "cost.net_price.private.by_income_level.110001-plus",
    "cost.avg_net_price.public",
    "cost.net_price.public.by_income_level.0-30000",
    "cost.net_price.public.by_income_level.30001-48000",
    "cost.net_price.public.by_income_level.48001-75000",
    "cost.net_price.public.by_income_level.75001-110000",
    "cost.net_price.public.by_income_level.110001-plus",
    "earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings",
    "earnings.6_yrs_after_entry.median",
    "earnings.6_yrs_after_entry.percent_greater_than_25000",
    "earnings.7_yrs_after_entry.mean_earnings",
    "earnings.7_yrs_after_entry.percent_greater_than_25000",
    "earnings.8_yrs_after_entry.mean_earnings",
    "earnings.8_yrs_after_entry.median_earnings",
    "earnings.8_yrs_after_entry.percent_greater_than_25000",
    "earnings.9_yrs_after_entry.mean_earnings",
    "earnings.9_yrs_after_entry.percent_greater_than_25000",
    "earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings",
    "earnings.10_yrs_after_entry.median",
    "earnings.10_yrs_after_entry.percent_greater_than_25000",
    "repayment.3_yr_repayment_suppressed.overall",
    "repayment.repayment_cohort.1_year_declining_balance",
    "repayment.1_yr_repayment.completers",
    "repayment.1_yr_repayment.noncompleters",
    "repayment.repayment_cohort.3_year_declining_balance",
    "repayment.3_yr_repayment.completers",
    "repayment.3_yr_repayment.noncompleters",
    "repayment.repayment_cohort.5_year_declining_balance",
    "repayment.5_yr_repayment.completers",
    "repayment.5_yr_repayment.noncompleters",
    "repayment.repayment_cohort.7_year_declining_balance",
    "repayment.7_yr_repayment.completers",
    "repayment.7_yr_repayment.noncompleters",
    "student.fafsa_sent.2_college_allyrs",
    "student.fafsa_sent.3_college_allyrs",
    "student.fafsa_sent.4_college_allyrs",
    "student.fafsa_sent.5plus_college_allyrs",
    "student.fafsa_sent.overall",
    "student.fafsa_sent.1_college",
    "student.fafsa_sent.2_colleges",
    "student.fafsa_sent.3_college",  # yes, should be 'colleges' but isn't
    "student.fafsa_sent.4_colleges",
    "student.fafsa_sent.5_or_more_colleges",
    "student.fafsa_sent.2_college_allyrs",
    "student.fafsa_sent.3_college_allyrs",
    "student.fafsa_sent.4_college_allyrs",
    "student.fafsa_sent.5plus_college_allyrs",
    "student.size",
    "student.enrollment.all",  # blank for many schools
    "student.retention_rate.four_year.full_time",
    "student.retention_rate.lt_four_year.full_time",
    "student.retention_rate.four_year.part_time",
    "student.retention_rate.lt_four_year.part_time",
    "student.demographics.veteran",  # blank for many schools
]
PROGRAM_FIELDS = [
    "programs.cip_4_digit.ope6_id",
    "programs.cip_4_digit.school.name",
    "programs.cip_4_digit.title",
    "programs.cip_4_digit.code",
    "programs.cip_4_digit.credential.level",
    "programs.cip_4_digit.debt.median_debt",
    "programs.cip_4_digit.debt.monthly_debt_payment",
    "programs.cip_4_digit.counts.titleiv",
    "programs.cip_4_digit.earnings.median_earnings",
]


def api_school_query(school_id, fields):
    """Explore endpoints; this is handy but no longer used in processing."""
    url = QUERY_URL.format(SCHOOLS_ROOT, school_id, API_KEY, fields)
    return requests.get(url).json()


def build_field_string():
    """Assemble fields for a fat API query."""
    latest_fields = [
        "latest.{}".format(field) for field in (YEAR_FIELDS + PROGRAM_FIELDS)
    ]
    fields = BASE_FIELDS + latest_fields
    return ",".join(fields)


def search_by_school_name(name):
    """Search api by school name, return school name, id, city, state."""
    fields = "id,school.name,school.city,school.state"
    url = "{0}?api_key={1}&school.name={2}&fields={3}".format(
        SCHOOLS_ROOT, API_KEY, name, fields
    )
    data = requests.get(url).json()["results"]
    return data


def calculate_group_percent(group1, group2):
    """Calculate group1's percentage of a two-group total."""
    if group1 + group2 == 0:
        return 0
    else:
        return round(group1 * 100.0 / (group1 + group2), 2)


def compile_school_programs(api_data):
    """Return a school's programs by popularity, and a program count."""
    program_data = {
        k: v for k, v in api_data.items() if "latest.academics.program_percentage." in k
    }
    program_tuples = sorted(
        [
            (v, k.replace("latest.academics.program_percentage.", ""))
            for k, v in program_data.items()
            if v != 0.0
        ],
        reverse=True,
    )
    popular = [PROGRAM_CATEGORIES.get(tup[1]) for tup in program_tuples]
    payload = {
        "programs": program_tuples,
        "program_count": len(program_tuples),
        "most_popular": popular,
    }
    return payload
