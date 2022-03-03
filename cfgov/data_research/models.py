import logging

from django.db import models

from wagtail.core.models import PageManager

from dateutil import parser

from v1.models import BrowsePage

logger = logging.getLogger(__name__)


class ConferenceRegistrationQuerySet(models.QuerySet):
    # TODO: In Django 1.9+, this logic can be optimized through use of
    # Django's built-in Postgres JSONFields. This will require migrating
    # the details field of the ConferenceRegistration model.
    #
    # return self.filter(
    #     details__attendee_type=self.IN_PERSON
    # )
    def in_person(self):
        return filter(
            lambda a: (
                a.details.get("attendee_type")
                == ConferenceRegistration.IN_PERSON
            ),
            self,
        )

    def virtual(self):
        return filter(
            lambda a: (
                a.details.get("attendee_type")
                == ConferenceRegistration.VIRTUAL
            ),
            self,
        )


class ConferenceRegistration(models.Model):
    IN_PERSON = "In person"
    VIRTUAL = "Virtually"

    created = models.DateTimeField(auto_now_add=True)
    govdelivery_code = models.CharField(max_length=250)
    details = models.JSONField()

    objects = ConferenceRegistrationQuerySet.as_manager()


# mortgage metadata models
class MortgageDataConstant(models.Model):
    """Constant values that Research can change via the admin."""

    name = models.CharField(max_length=255)
    slug = models.CharField(
        max_length=255, blank=True, help_text="OPTIONAL SLUG"
    )
    value = models.IntegerField(null=True, blank=True)
    date_value = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "CHOOSE THE LAST MONTH OF DATA TO DISPLAY "
            "(AND SELECT THE FIRST DAY OF THAT MONTH)"
        ),
    )
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return "{} ({}), updated {}".format(self.name, self.slug, self.updated)

    @classmethod
    def get_thresholds(cls):
        """Returns the constants we need to validate geo ares."""
        threshold_count = cls.objects.get(name="threshold_count").value
        threshold_year = cls.objects.get(name="threshold_year").value
        return (threshold_count, threshold_year)

    class Meta:
        ordering = ["name"]


class MortgageMetaData(models.Model):
    """
    Metadata values, stored as json, and made available in the API.
    """

    name = models.CharField(max_length=255)
    json_value = models.JSONField(blank=True, null=True)
    note = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return "{}, updated {}".format(self.name, self.updated)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Mortgage metadata"


# mortgage geo models


class State(models.Model):
    fips = models.CharField(max_length=2, blank=True, db_index=True)
    name = models.CharField(max_length=128, blank=True, db_index=True)
    abbr = models.CharField(max_length=2)
    ap_abbr = models.CharField(
        max_length=20, help_text="The AP Stylebook's state abbreviation"
    )
    counties = models.JSONField(
        blank=True, help_text="FIPS list of counties in the state"
    )
    non_msa_counties = models.JSONField(
        blank=True,
        help_text="FIPS list of counties in the state that are not in an MSA",
    )
    msas = models.JSONField(
        blank=True, help_text="FIPS list of MSAs in the state"
    )
    non_msa_valid = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.fips)

    def validate_non_msas(self):
        """
        Using parameters stored as constants, determines whether
        a state's non-msa counties, taken together, have sufficient data
        to be included in visualizations and downloads.
        """
        (
            threshold_count,
            threshold_year,
        ) = MortgageDataConstant.get_thresholds()
        records = self.nonmsamortgagedata_set.filter(date__year=threshold_year)
        if not self.non_msa_counties:
            self.non_msa_valid = False
            self.save()
            return
        annual_sum = sum(record.total for record in records if record.total)
        monthly_average = annual_sum * 1.0 / records.count()
        if monthly_average >= threshold_count:
            self.non_msa_valid = True
        else:
            self.non_msa_valid = False
        self.save()

    class Meta:
        ordering = ["name"]


class MetroArea(models.Model):
    """Model for Metropolitan Statistical Areas, or MSAs."""

    fips = models.CharField(max_length=6, blank=True, db_index=True)
    name = models.CharField(max_length=128, blank=True)
    counties = models.JSONField(
        blank=True, help_text="FIPS list of counties in the MSA"
    )
    states = models.JSONField(
        blank=True, help_text="FIPS list of states touched by MSA"
    )
    valid = models.BooleanField()

    def validate(self):
        """
        Using parameters stored as constants, determines whether a metro area
        has sufficient data to be included in visualizations and downloads.
        """
        (
            threshold_count,
            threshold_year,
        ) = MortgageDataConstant.get_thresholds()
        records = self.msamortgagedata_set.filter(date__year=threshold_year)
        annual_sum = sum(record.total for record in records)
        monthly_average = annual_sum * 1.0 / records.count()
        if monthly_average >= threshold_count:
            self.valid = True
        else:
            self.valid = False
        self.save()

    def __str__(self):
        return "{} ({})".format(self.name, self.fips)

    class Meta:
        ordering = ["name"]


class County(models.Model):
    """Model for the smallest geophraphical unit in our mortgage data."""

    fips = models.CharField(max_length=6, blank=True, db_index=True)
    name = models.CharField(max_length=128, blank=True)
    state = models.ForeignKey(
        State, blank=True, null=True, on_delete=models.SET_NULL
    )
    valid = models.BooleanField()

    def validate(self):
        """
        Using parameters stored as constants, determines whether a county
        has sufficient data to be included in visualizations and downloads.
        """
        (
            threshold_count,
            threshold_year,
        ) = MortgageDataConstant.get_thresholds()
        records = self.countymortgagedata_set.filter(date__year=threshold_year)
        annual_sum = sum(record.total for record in records)
        monthly_average = (
            annual_sum * 1.0 / records.count() if records.count() > 0 else 0
        )
        if monthly_average >= threshold_count:
            self.valid = True
        else:
            self.valid = False
        self.save()

    def __str__(self):
        return "{}, {} ({})".format(self.name, self.state.abbr, self.fips)


# mortgage data models for counts, aggregations and averages


class MortgageBase(models.Model):
    """An abstract model base for mortgage data records and calculations."""

    fips = models.CharField(max_length=6, blank=True, db_index=True)
    date = models.DateField(blank=True, db_index=True)
    total = models.IntegerField(null=True)
    current = models.IntegerField(null=True)
    thirty = models.IntegerField(null=True)
    sixty = models.IntegerField(null=True)
    ninety = models.IntegerField(null=True)
    other = models.IntegerField(null=True)

    class Meta:
        abstract = True
        ordering = ["date"]

    @property
    def county_list(self):
        """
        Each child model, except CountyMortgageData, should define
        its own list of FIPS or CBSA codes to be aggregated.
        """
        return []

    def aggregate_data(self):
        count_fields = {
            "total": 0,
            "current": 0,
            "thirty": 0,
            "sixty": 0,
            "ninety": 0,
            "other": 0,
        }
        if self.county_list:
            county_records = CountyMortgageData.objects.filter(
                date=self.date, fips__in=self.county_list
            )
            for county in county_records:
                for field in count_fields:
                    count_fields[field] += getattr(county, field)
            for field in count_fields:
                setattr(self, field, count_fields[field])
            self.save()
        elif type(self) == NonMSAMortgageData:
            for field in count_fields:
                setattr(self, field, count_fields[field])
            self.save()

    def time_series(self, days_late):
        if days_late == "30-89":
            return {"date": self.epoch, "value": self.percent_30_60}
        else:
            return {"date": self.epoch, "value": self.percent_90}

    @property
    def percent_90(self):
        """Return decimal percentage of loans 90-plus days delinquent."""
        if self.total == 0:
            return 0
        else:
            return self.ninety * 1.0 / self.total

    @property
    def percent_30_60(self):
        """Combine thirty and sixty and returns decimal percent of total."""
        if self.total == 0:
            return 0
        else:
            return (self.thirty + self.sixty) * 1.0 / self.total

    @property
    def epoch(self):
        return int(self.date.strftime("%s")) * 1000


class CountyMortgageData(MortgageBase):
    """
    A bare-bones model to store county mortgage performance values for every
    county and sampling month. Our atomic data point, Updated quarterly.
    """

    county = models.ForeignKey(County, null=True, on_delete=models.CASCADE)


class MSAMortgageData(MortgageBase):
    """
    Aggregate mortgage performance data from
    a set of counties included in a metro area.
    """

    msa = models.ForeignKey(MetroArea, null=True, on_delete=models.CASCADE)

    @property
    def county_list(self):
        """Return a list of county FIPS codes to be aggregated"""
        return self.msa.counties


class StateMortgageData(MortgageBase):
    """
    Aggregate data for all counties in a given state.
    """

    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)

    @property
    def county_list(self):
        """Returns a list of county FIPS codes to be aggregated"""
        return self.state.counties


class NonMSAMortgageData(MortgageBase):
    """
    Aggregate state data for counties that do not belong to an MSA.
    """

    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)

    @property
    def county_list(self):
        """Return a list of county FIPS codes to be aggregated"""
        return self.state.non_msa_counties


class NationalMortgageData(MortgageBase):
    """Aggregate national data for a given date."""

    def aggregate_data(self):
        """Calculates aggregate values for all states, by date"""
        count_fields = {
            "total": 0,
            "current": 0,
            "thirty": 0,
            "sixty": 0,
            "ninety": 0,
            "other": 0,
        }
        state_records = StateMortgageData.objects.filter(date=self.date)
        for state in state_records:
            for field in count_fields:
                count_fields[field] += getattr(state, field)
        for field in count_fields:
            setattr(self, field, count_fields[field])
        self.save()


class MortgagePerformancePage(BrowsePage):
    """
    A model for data_research pages about mortgage delinquency
    and related data visualizations.
    """

    objects = PageManager()
    template = "browse-basic/index.html"

    def get_mortgage_meta(self):
        meta_names = ["sampling_dates", "download_files"]
        meta_set = MortgageMetaData.objects.filter(name__in=meta_names)
        meta = {obj.name: obj.json_value for obj in meta_set}
        thru_date = parser.parse(meta["sampling_dates"][-1])
        from_date = parser.parse(meta["sampling_dates"][0])
        meta["thru_month"] = thru_date.strftime("%Y-%m")
        meta["thru_month_formatted"] = thru_date.strftime("%B&nbsp;%Y")
        meta["from_month_formatted"] = from_date.strftime("%B&nbsp;%Y")
        meta["pub_date_formatted"] = meta.get("download_files")[
            meta["thru_month"]
        ]["pub_date"]
        download_dates = sorted(meta["download_files"].keys(), reverse=True)
        meta["archive_dates"] = download_dates[1:]
        return meta

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_mortgage_meta())
        if "30-89" in self.url:
            context.update(
                {"delinquency": "percent_30_60", "time_frame": "30-89"}
            )
        elif "90" in self.url:
            context.update({"delinquency": "percent_90", "time_frame": "90"})
        return context

    class Media:
        css = ["secondary-navigation.css"]


def validate_counties():
    for each in County.objects.all():
        each.validate()
    total = County.objects.count()
    valid = County.objects.filter(valid=True).count()
    if total != 0:
        logger.info(
            "{} counties of {} were found to be valid -- {}%)".format(
                valid, total, round((valid * 100.0 / total), 1)
            )
        )
