# -*- coding: utf-8 -*-
import datetime
import json
import smtplib
from collections import OrderedDict
from csv import writer as csw
from string import Template

from django.contrib.postgres.fields import JSONField
from django.core.mail import send_mail
from django.db import models

import requests


# Our database has a fake school for demo purposes
# It should be discoverable via search and API calls, but should be excluded
# from cohort calculations and from College Scorecard API updates.
FAKE_SCHOOL_PK = 999999
# Our database also has 49 entries for school or school system home offices,
# which should be excluded from school processing and comparisons.
OFFICE_IDS = [
    100733, 105136, 108056, 110501, 112376, 112817, 117681, 117900, 121178,
    122320, 122782, 124557, 125019, 125222, 126100, 128300, 130882, 141963,
    144500, 144777, 149240, 151485, 159638, 161280, 166665, 178439, 181747,
    182519, 183327, 190035, 195827, 199175, 214661, 222497, 228732, 229090,
    231156, 242671, 403399, 438665, 443368, 446978, 448336, 448381, 454218,
    461087, 481191, 483090, 485467,
]
DEFAULT_EXCLUSIONS = OFFICE_IDS + [FAKE_SCHOOL_PK]
REGION_MAP = {'MW': ['IL', 'IN', 'IA', 'KS', 'MI', 'MN',
                     'MO', 'NE', 'ND', 'OH', 'SD', 'WI'],
              'NE': ['CT', 'ME', 'MA', 'NH', 'NJ',
                     'NY', 'PA', 'RI', 'VT'],
              'SO': ['AL', 'AR', 'DE', 'DC', 'FL', 'GA', 'KY', 'LA', 'MD',
                     'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV'],
              'WE': ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM',
                     'OR', 'UT', 'WA', 'WY']
              }

CONTROL_MAP = {'1': 'Public',
               '2': 'Private',
               '3': 'For-profit'}

REGION_NAMES = {'MW': 'Midwest',
                'NE': "Northeast",
                'SO': 'South',
                'WE': 'West'}

# Highest-awarded values from the DOE and our CSV spec
# For our API, we treat anything above bachelor's as graduate-degree-granting
HIGHEST_DEGREES = {
    '0': "Non-degree-granting",
    '1': 'Certificate',
    '2': "Associate degree",
    '3': "Bachelor's degree",
    '4': "Graduate degree"
}

# Legacy DOE classifications of post-secondary degree levels
LEVELS = {
    '1': "Program of less than 1 academic year",
    '2': "Program of at least 1 but less than 2 academic years",
    '3': "Associate degree",
    '4': "Program of at least 2 but less than 4 academic years",
    '5': "Bachelor's degree",
    '6': "Post-baccalaureate certificate",
    '7': "Master's degree",
    '8': "Post-master's certificate",
    '17': "Doctor's degree-research/scholarship",
    '18': "Doctor's degree-professional practice",
    '19': "Doctor's degree-other"
}

# Dept. of Ed program degree levels specific to new program data in 2019
PROGRAM_LEVELS = {
    '1': "Certificate",
    '2': "Associate degree",
    '3': "Bachelor's degree",
    '4': "Post-baccalaureate certificate",
    '5': "Master's degree",
    '6': "Doctoral degree",
    '7': "First professional degree",
    '8': "Graduate/professional certificate",
}

NOTIFICATION_TEMPLATE = Template("""Disclosure notification for offer ID $oid\n\
    timestamp: $time\n\
    errors: $errors\n\
If errors are "none," the disclosure is confirmed.\
""")


def get_region(school):
    """return a school's region based on state"""
    for region in REGION_MAP:
        if school.state in REGION_MAP[region]:
            return region
    return ''


def make_divisible_by_6(value):
    """Makes sure a value, such as program_length, is divisible by 6"""
    if not value or value % 6 == 0:
        return value
    else:
        return value + (6 - (value % 6))


class ConstantRate(models.Model):
    """Rate values that generally only change annually"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,
                            blank=True,
                            help_text="VARIABLE NAME FOR JS")
    value = models.DecimalField(max_digits=6, decimal_places=5)
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return "{} ({}), updated {}".format(self.name, self.slug, self.updated)

    class Meta:
        ordering = ['slug']


class ConstantCap(models.Model):
    """Cap values that generally only change annually"""
    name = models.CharField(max_length=255)
    slug = models.CharField(
        max_length=255,
        blank=True,
        help_text="VARIABLE NAME FOR JS")
    value = models.IntegerField()
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return "{} ({}), updated {}".format(self.name, self.slug, self.updated)

    class Meta:
        ordering = ['slug']


# original data_json fields:
# ALIAS -- not needed, DELETE
# AVGMONTHLYPAY
# AVGSTULOANDEBT
# AVGSTULOANDEBTRANK -- not needed, DELETE
# BADALIAS -- not needed, DELETE
# BAH 1356 -- not needed, DELETE
# BOOKS
# CITY (now school.city)
# CONTROL (now school.control)
# DEFAULTRATE
# GRADRATE -- now school.grad_rate
# GRADRATERANK -- not needed, DELETE
# INDICATORGROUP
# KBYOSS (now school.kbyoss) -- not needed, DELETE
# MEDIANDEBTCOMPLETER # new in 2015
# NETPRICE110K -- not needed, DELETE
# NETPRICE3OK -- not needed, DELETE
# NETPRICE48K -- not needed, DELETE
# NETPRICE75K -- not needed, DELETE
# NETPRICEGENERAL -- not needed, DELETE
# NETPRICEOK -- not needed, DELETE
# OFFERAA
# OFFERBA
# OFFERGRAD
# ONCAMPUSAVAIL
# ONLINE (now school.online)
# OTHEROFFCAMPUS
# OTHERONCAMPUS
# OTHERWFAMILY
# RETENTRATE -- not needed, DELETE
# RETENTRATELT4 # new in 2015 -- not needed, DELETE
# REPAY3YR # new in 2015
# ROOMBRDOFFCAMPUS
# ROOMBRDONCAMPUS
# SCHOOL (now school.primary_alias)
# SCHOOL_ID (now school.pk)
# STATE (now school.state)
# TUITIONGRADINDIS
# TUITIONGRADINS
# TUITIONGRADOSS
# TUITIONUNDERINDIS
# TUITIONUNDERINS
# TUITIONUNDEROSS
# ZIP (now school.zip5)


class Contact(models.Model):
    """school endpoint or email to which we send confirmations"""
    contacts = models.TextField(
        help_text="COMMA-SEPARATED LIST OF EMAILS",
        blank=True)
    endpoint = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    internal_note = models.TextField(blank=True)

    def __str__(self):
        return ", ".join(
            [bit for bit in [self.contacts, self.endpoint] if bit]
        )


def format_for_null(value):
    """If a Python value is None, we want it to convert to null in json."""
    if value is None:
        return value
    else:
        return "{}".format(value)


class School(models.Model):
    """
    Represents a school
    """
    school_id = models.IntegerField(primary_key=True)
    ope6_id = models.IntegerField(blank=True, null=True)
    ope8_id = models.IntegerField(blank=True, null=True)
    settlement_school = models.CharField(
        max_length=100,
        blank=True,
        default='')
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    data_json = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip5 = models.CharField(max_length=5, blank=True)
    enrollment = models.IntegerField(blank=True, null=True)
    accreditor = models.CharField(max_length=255, blank=True)
    ownership = models.CharField(max_length=255, blank=True)
    control = models.CharField(
        max_length=50,
        blank=True,
        help_text="'Public', 'Private' or 'For-profit'")
    url = models.TextField(blank=True)
    degrees_predominant = models.TextField(blank=True)
    degrees_highest = models.TextField(blank=True)
    program_count = models.IntegerField(blank=True, null=True)
    program_most_popular = JSONField(blank=True, null=True)
    main_campus = models.NullBooleanField()
    online_only = models.NullBooleanField()
    operating = models.BooleanField(default=True)
    under_investigation = models.BooleanField(
        default=False,
        help_text="Heightened Cash Monitoring 2")
    KBYOSS = models.BooleanField(default=False)  # shopping-sheet participant
    grad_rate_4yr = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True, null=True)
    grad_rate_lt4 = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True, null=True)
    grad_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True, null=True,
        help_text="A 2-YEAR POOLED VALUE")
    repay_3yr = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        blank=True, null=True,
        help_text="GRADS WITH A DECLINING BALANCE AFTER 3 YRS")
    repay_5yr = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        blank=True, null=True,
        help_text="GRADS WITH A DECLINING BALANCE AFTER 5 YRS")
    default_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True, null=True,
        help_text="LOAN DEFAULT RATE AT 5 YRS")
    median_total_debt = models.DecimalField(
        max_digits=7,
        decimal_places=1,
        blank=True, null=True,
        help_text="MEDIAN STUDENT DEBT 10 YRS AFTER ENROLLING")
    median_monthly_debt = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True, null=True,
        help_text=("MEDIAN STUDENT MONTHLY DEBT"))
    median_annual_pay = models.IntegerField(
        blank=True,
        null=True,
        help_text=("MEDIAN PAY 10 YRS AFTER ENTRY"))
    median_annual_pay_6yr = models.IntegerField(
        blank=True,
        null=True,
        help_text=("MEDIAN PAY 6 YRS AFTER ENTRY"))
    avg_net_price = models.IntegerField(
        blank=True,
        null=True,
        help_text="OVERALL AVERAGE")
    avg_net_price_slices = JSONField(blank=True, null=True)
    tuition_out_of_state = models.IntegerField(blank=True, null=True)
    tuition_in_state = models.IntegerField(blank=True, null=True)
    offers_perkins = models.BooleanField(default=False)
    cohort_ranking_by_control = JSONField(blank=True, null=True)
    cohort_ranking_by_highest_degree = JSONField(blank=True, null=True)
    cohort_ranking_by_state = JSONField(blank=True, null=True)
    associate_transfer_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True, null=True,
        help_text=(
            "Transfer rate for first-time, full-time students at "
            "less-than-four-year institutions "
            "(150% of expected time to completion)"))

    def as_json(self):
        """
        Deliver pertinent data points as json.

        Fields marked below as "legacy" may duplicate other fields
        but are maintained for backward compatibility, for the sake of
        the orignal for-profit version of the tool.
        """

        region = get_region(self)
        ordered_out = OrderedDict()
        jdata = json.loads(self.data_json)
        dict_out = {
            'books': jdata['BOOKS'],
            'city': self.city,
            'cohortRankByControl': self.cohort_ranking_by_control,
            'cohortRankByHighestDegree': self.cohort_ranking_by_highest_degree,
            'cohortRankByState': self.cohort_ranking_by_state,
            'control': self.control,
            'defaultRate': format_for_null(self.default_rate),  # legacy
            'enrollment': self.enrollment,
            'gradRate': format_for_null(self.grad_rate),  # legacy
            'highestDegree': self.get_highest_degree(),
            'medianAnnualPay': self.median_annual_pay,
            'medianAnnualPay6Yr': self.median_annual_pay_6yr,
            'medianMonthlyDebt': format_for_null(self.median_monthly_debt),
            'medianTotalDebt': format_for_null(self.median_total_debt),
            'netPriceAvg': self.avg_net_price,
            'netPriceAvgSlices': self.avg_net_price_slices,
            'nicknames': ", ".join([nick.nickname for nick
                                    in self.nickname_set.all()]),
            'offersPerkins': self.offers_perkins,
            'onCampusAvail': jdata['ONCAMPUSAVAIL'],
            'online': self.online_only,
            'otherOffCampus': jdata['OTHEROFFCAMPUS'],
            'otherOnCampus': jdata['OTHERONCAMPUS'],
            'otherWFamily': jdata['OTHERWFAMILY'],
            'programCodes': self.program_codes,
            'programCount': self.program_count,
            'programsPopular': self.program_most_popular,
            'predominantDegree': self.get_predominant_degree(),
            'rateAssociateTransfer': format_for_null(
                self.associate_transfer_rate),
            'rateDefault': format_for_null(self.default_rate),
            'rateGraduation': format_for_null(self.grad_rate),
            'rateRepay3yr': format_for_null(self.repay_3yr),
            'region': region,
            'repay3yr': format_for_null(self.repay_3yr),  # legacy
            'roomBrdOffCampus': jdata['ROOMBRDOFFCAMPUS'],
            'roomBrdOnCampus': jdata['ROOMBRDONCAMPUS'],
            'school': self.primary_alias,
            'schoolID': self.pk,
            'schoolSalary': self.median_annual_pay,
            'settlementSchool': self.settlement_school,
            'state': self.state,
            'tuitionGradInDis': jdata['TUITIONGRADINDIS'],
            'tuitionGradInS': jdata['TUITIONGRADINS'],
            'tuitionGradOss': jdata['TUITIONGRADOSS'],
            'tuitionUnderInDis': jdata['TUITIONUNDERINDIS'],
            'tuitionUnderInS': self.tuition_in_state,
            'tuitionUnderOoss': self.tuition_out_of_state,
            'underInvestigation': self.under_investigation,
            'url': self.url,
            'zip5': self.zip5,

        }
        for key in sorted(dict_out.keys()):
            ordered_out[key] = dict_out[key]
        return json.dumps(ordered_out)

    def __str__(self):
        return self.primary_alias + " ({})".format(self.school_id)

    @property
    def program_codes(self):
        # We're only insterested in program data with salary included
        payload = {}
        live_programs = self.program_set.filter(
            test=False).exclude(level='').exclude(salary=None)
        graduate = [p for p in live_programs if int(p.level) > 3]
        undergrad = [p for p in live_programs if p not in graduate]
        program_sets = {
            'graduate': graduate,
            'undergrad': undergrad
        }
        for level in program_sets:
            payload.update({
                level: [{
                    'code': p.program_code,
                    'name': p.program_name.strip('.'),
                    'level': PROGRAM_LEVELS.get(p.level),
                    'salary': p.salary}
                    for p in program_sets[level]
                ]
            })
        return payload

    def get_predominant_degree(self):
        predominant = ''
        if (self.degrees_predominant
                and self.degrees_predominant in HIGHEST_DEGREES):
            predominant = HIGHEST_DEGREES[self.degrees_predominant]
        return predominant

    def get_highest_degree(self):
        highest = ''
        if (self.degrees_highest
                and self.degrees_highest in HIGHEST_DEGREES):
            highest = HIGHEST_DEGREES[self.degrees_highest]
        return highest

    def convert_ope6(self):
        if self.ope6_id:
            digits = len(str(self.ope6_id))
            if digits < 6:
                return ('0' * (6 - digits)) + str(self.ope6_id)
            else:
                return str(self.ope6_id)
        else:
            return ''

    def convert_ope8(self):
        if self.ope8_id:
            digits = len(str(self.ope8_id))
            if digits < 8:
                return ('0' * (8 - digits)) + str(self.ope8_id)
            else:
                return str(self.ope8_id)
        else:
            return ''

    @property
    def primary_alias(self):
        if len(self.alias_set.values()) != 0:
            return self.alias_set.get(is_primary=True).alias
        else:
            return 'Not Available'

    @property
    def nicknames(self):
        return ", ".join([nick.nickname for nick in self.nickname_set.all()])


class DisclosureBase(models.Model):
    """Abstract base class for disclosure-related interactions"""
    url = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def parsed_url(self):
        """parses a disclosure URL and returns a field:value dict"""
        data = {}
        if not self.url or '?' not in self.url:
            return data
        split_fields = self.url.replace(
            '#info-right', '').split('?')[1].split('&')
        for field in split_fields:
            pair = field.split('=')
            data[pair[0]] = pair[1]
        return data

    @property
    def school(self):
        """Returns a school object, derived from a feedback url"""
        if not self.url:
            return None
        row = self.parsed_url
        if row and row.get('iped'):
            return School.objects.get(pk=row['iped'])
        else:
            return None

    @property
    def unmet_cost(self):
        """Calculates and returns a disclosure's unmet cost"""
        url_data = self.parsed_url
        if not url_data:
            return None

        def total_fields(field_list):
            total = 0
            for field in field_list:
                if field in url_data.keys() and url_data.get(field, '') != '':
                    try:
                        total += int(url_data[field])
                    except ValueError:
                        pass
            return total

        cost_fields = ['tuit', 'hous', 'book', 'tran', 'othr']
        asset_fields = ['pelg', 'gib', 'mta', 'schg', 'othg', 'stag', 'wkst',
                        'prvl', 'ppl', 'perl', 'gpl', 'insl', 'subl', 'unsl']
        total_costs = total_fields(cost_fields)
        total_assets = total_fields(asset_fields)
        return total_costs - total_assets

    @property
    def cost_error(self):
        """Return 1 or 0: Is total-cost less than tuition?"""
        url_data = self.parsed_url
        if url_data:
            totl = url_data.get('totl') or 0
            tuit = url_data.get('tuit') or 0
            if int(totl) < int(tuit):
                return 1
            else:
                return 0
        else:
            return 0

    @property
    def tuition_plan(self):
        """Return amount of tuition plan or None"""
        url_data = self.parsed_url
        if url_data and url_data.get('insl'):
            try:
                return int(url_data.get('insl'))
            except ValueError:
                return None


class Feedback(DisclosureBase):
    """
    User-submitted feedback
    """
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class Notification(DisclosureBase):
    """record of a disclosure verification"""
    institution = models.ForeignKey(School, on_delete=models.CASCADE)
    oid = models.CharField(max_length=40)
    timestamp = models.DateTimeField()
    errors = models.CharField(max_length=255)
    emails = models.TextField(blank=True,
                              help_text="COMMA-SEPARATED STRING OF EMAILS")
    sent = models.BooleanField(default=False)
    log = models.TextField(blank=True)

    def __str__(self):
        return "{0} {1} ({2})".format(
            self.oid,
            self.institution.primary_alias,
            self.institution.pk
        )

    def notify_school(self):
        school = self.institution
        if not school.settlement_school:
            nonmsg = "No notification required; {} is not a settlement school"
            return nonmsg.format(school.primary_alias)
        payload = {
            'oid': self.oid,
            'time': self.timestamp.isoformat(),
            'errors': self.errors
        }
        now = datetime.datetime.now()
        no_contact_msg = (
            "School notification failed: "
            "No endpoint or email info {}".format(now))
        # we prefer to use endpount notification, so use it first if existing
        if school.contact:
            if school.contact.endpoint:
                endpoint = school.contact.endpoint
                if type(endpoint) == str:
                    endpoint = endpoint.encode('utf-8')
                try:
                    resp = requests.post(endpoint, data=payload, timeout=10)
                except requests.exceptions.ConnectionError as e:
                    exmsg = ("Error: connection error at school "
                             "{} {}\n".format(now, e))
                    self.log = self.log + exmsg
                    self.save()
                    return exmsg
                except requests.exceptions.Timeout:
                    exmsg = ("Error: connection with school "
                             "timed out {}\n".format(now))
                    self.log = self.log + exmsg
                    self.save()
                    return exmsg
                except requests.exceptions.RequestException as e:
                    exmsg = ("Error: request error at school: "
                             "{} {}\n".format(now, e))
                    self.log = self.log + exmsg
                    self.save()
                    return exmsg
                else:
                    if resp.ok:
                        self.sent = True
                        self.log = ("School notified "
                                    "via endpoint {}".format(now))
                        self.save()
                        return self.log
                    else:
                        msg = (
                            "Send attempted: {}\nURL: {}\n"
                            "response reason: {}\nstatus_code: {}\n"
                            "content: {}\n\n".format(
                                now,
                                endpoint.decode('utf-8'),
                                resp.reason,
                                resp.status_code,
                                resp.content)
                        )
                        self.log = self.log + msg
                        self.save()
                        return "Notification failed: {}".format(msg)
            elif school.contact.contacts:
                try:
                    send_mail("CFPB disclosure notification",
                              NOTIFICATION_TEMPLATE.substitute(payload),
                              "no-reply@cfpb.gov",
                              [email for email
                               in school.contact.contacts.split(',')],
                              fail_silently=False)
                    self.sent = True
                    self.emails = school.contact.contacts
                    self.log = ("School notified via email "
                                "at {}".format(self.emails))
                    self.save()
                    return self.log
                except smtplib.SMTPException as e:
                    email_fail_msg = ("School email notification "
                                      "failed on {}\n"
                                      "Error: {}".format(now, e))
                    self.log = self.log + email_fail_msg
                    self.save()
                    return email_fail_msg
            else:
                self.log = self.log + no_contact_msg
                self.save()
                return no_contact_msg
        else:
            self.log = self.log + no_contact_msg
            self.save()
            return no_contact_msg


class Program(models.Model):
    """
    Cost and outcome info for an individual course of study at a school
    """
    DEBT_NOTE = "TITLEIV_DEBT + PRIVATE_DEBT + INSTITUTIONAL_DEBT"
    institution = models.ForeignKey(School, on_delete=models.CASCADE)
    accreditor = models.CharField(max_length=255, blank=True)
    program_name = models.CharField(max_length=255)
    program_code = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=255, blank=True)
    level_name = models.CharField(max_length=255, blank=True, null=True)
    campus = models.CharField(max_length=255, blank=True)
    cip_code = models.CharField(max_length=255, blank=True)
    soc_codes = models.CharField(max_length=255, blank=True)
    total_cost = models.IntegerField(
        blank=True, null=True, help_text="COMPUTED")
    time_to_complete = models.IntegerField(
        blank=True, null=True, help_text="IN MONTHS")
    completion_rate = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=2)
    completion_cohort = models.IntegerField(
        blank=True, null=True, help_text="COMPLETION COHORT")
    completers = models.IntegerField(
        blank=True, null=True, help_text="COMPLETERS OF THE PROGRAM")
    titleiv_debt = models.IntegerField(blank=True, null=True)
    private_debt = models.IntegerField(blank=True, null=True)
    institutional_debt = models.IntegerField(blank=True, null=True)
    mean_student_loan_completers = models.IntegerField(
        blank=True, null=True, help_text=DEBT_NOTE)
    median_student_loan_completers = models.IntegerField(
        blank=True, null=True, help_text=DEBT_NOTE)
    median_monthly_debt = models.IntegerField(
        blank=True, null=True,
        help_text="MEDIAN MONTHLY PAYMENT FOR A 10-YEAR LOAN")
    default_rate = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=2)
    salary = models.IntegerField(
        blank=True, null=True, help_text='MEDIAN SALARY')
    program_length = models.IntegerField(
        blank=True, null=True, help_text="IN MONTHS")
    tuition = models.IntegerField(
        blank=True, null=True)
    fees = models.IntegerField(
        blank=True, null=True)
    housing = models.IntegerField(
        blank=True, null=True, help_text="HOUSING & MEALS")
    books = models.IntegerField(
        blank=True, null=True, help_text="BOOKS & SUPPLIES")
    transportation = models.IntegerField(blank=True, null=True)
    other_costs = models.IntegerField(blank=True, null=True)
    job_rate = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=2,
        help_text="COMPLETERS WHO GET RELATED JOB")
    job_note = models.TextField(
        blank=True, help_text="EXPLANATION FROM SCHOOL")
    test = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.program_name, self.institution)

    def get_level(self):
        level = ''
        if self.level and str(self.level) in HIGHEST_DEGREES:
            level = HIGHEST_DEGREES[str(self.level)]
        return level

    def as_json(self):
        ordered_out = OrderedDict()
        dict_out = {
            'accreditor': self.accreditor,
            'books': self.books,
            'campus': self.campus,
            'cipCode': self.cip_code,
            'completionRate': "{0}".format(self.completion_rate),
            'completionCohort': self.completion_cohort,
            'completers': self.completers,
            'defaultRate': "{0}".format(self.default_rate),
            'fees': self.fees,
            'housing': self.housing,
            'institution': self.institution.primary_alias,
            'institutionalDebt': self.institutional_debt,
            'jobNote': self.job_note,
            'jobRate': format_for_null(self.job_rate),
            'level': self.level,
            'levelName': PROGRAM_LEVELS.get(self.level),
            'meanStudentLoanCompleters': self.mean_student_loan_completers,
            'medianMonthlyDebt': self.median_monthly_debt,
            'medianStudentLoanCompleters': self.median_student_loan_completers,
            'privateDebt': self.private_debt,
            'programCode': self.program_code,
            'programLength': make_divisible_by_6(self.program_length),
            'programName': self.program_name.strip('.'),
            'programSalary': self.salary,
            'schoolID': self.institution.school_id,
            'socCodes': self.soc_codes,
            'timeToComplete': self.time_to_complete,
            'titleIVDebt': self.titleiv_debt,
            'totalCost': self.total_cost,
            'transportation': self.transportation,
            'tuition': self.tuition,
        }
        for key in sorted(dict_out.keys()):
            ordered_out[key] = dict_out[key]

        return json.dumps(ordered_out)

    def as_csv(self, csvpath):
        """Output a CSV representation of a program"""
        headings = [
            'ipeds_unit_id',
            'ope_id',
            'program_code',
            'program_name',
            'program_length',
            'program_level',
            'accreditor',
            'median_salary',
            'average_time_to_complete',
            'books_supplies',
            'campus_name',
            'cip_code',
            'completion_rate',
            'completion_cohort',
            'completers',
            'default_rate',
            'job_placement_rate',
            'job_placement_note',
            'mean_student_loan_completers',
            'median_student_loan_completers',
            'soc_codes',
            'total_cost',
            'tuition_fees',
            'test'
        ]
        with open(csvpath, 'w') as f:
            writer = csw(f)
            writer.writerow(headings)
            writer.writerow([
                self.institution.school_id,
                '',
                self.program_code,
                self.program_name,
                self.program_length,
                self.level,
                self.accreditor,
                self.salary,
                self.time_to_complete,
                self.books,
                self.campus,
                self.cip_code,
                "{}".format(self.completion_rate),
                self.completion_cohort,
                self.completers,
                "{0}".format(self.default_rate),
                "{0}".format(self.job_rate),
                self.job_note,
                self.mean_student_loan_completers,
                self.median_student_loan_completers,
                self.soc_codes,
                self.total_cost,
                self.tuition,
                self.test
            ])


class Alias(models.Model):
    """
    One of potentially several names for a school
    """
    institution = models.ForeignKey(School, on_delete=models.CASCADE)
    alias = models.TextField()
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return "{} (alias for {})".format(self.alias, self.institution)

    class Meta:
        verbose_name_plural = "Aliases"


class Nickname(models.Model):
    """
    One of potentially several nicknames for a school
    """
    institution = models.ForeignKey(School, on_delete=models.CASCADE)
    nickname = models.TextField()
    is_female = models.BooleanField(default=False)

    def __str__(self):
        return "{} (nickname for {})".format(
            self.nickname, self.institution)

    class Meta:
        ordering = ['nickname']


class BAHRate(models.Model):
    """
    Basic Allowance for Housing (BAH) rates are zipcode-specific.
    Used in GI Bill data and may go away.
    """
    zip5 = models.CharField(max_length=5)
    value = models.IntegerField()
