import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from data_research.models import (
    County,
    CountyMortgageData,
    MetroArea,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    State,
    StateMortgageData,
)


DAYS_LATE_RANGE = ["30-89", "90"]


class MetaData(APIView):
    """
    View for delivering mortgage metadata based on latest data update.
    """

    renderer_classes = (JSONRenderer,)

    def get(self, request, meta_name):
        try:
            record = MortgageMetaData.objects.get(name=meta_name)
        except MortgageMetaData.DoesNotExist:
            return Response("No metadata object found.")
        meta_json = record.json_value
        return Response(meta_json)


class TimeSeriesNational(APIView):
    """
    View for delivering national time-series data
    from the mortgage performance dataset.
    """

    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request, days_late):
        if days_late not in DAYS_LATE_RANGE:
            return Response("Unknown delinquency range")
        records = NationalMortgageData.objects.all()
        data = {
            "meta": {"name": "United States", "fips_type": "national"},
            "data": [record.time_series(days_late) for record in records],
        }
        return Response(data)


class TimeSeriesData(APIView):
    """
    View for delivering geo-based time-series data
    from the mortgage performance dataset.
    """

    renderer_classes = (JSONRenderer,)

    def get(self, request, days_late, fips):
        """
        Return a FIPS-based slice of base data as a json timeseries.
        """
        if days_late not in DAYS_LATE_RANGE:
            return Response("Unknown delinquency range")
        reference_lists = {
            entry: MortgageMetaData.objects.get(name=entry).json_value
            for entry in ["allowlist", "msa_fips", "non_msa_fips"]
        }
        if fips not in reference_lists["allowlist"]:
            return Response("FIPS code not found or not valid.")
        if len(fips) == 2:
            state = State.objects.get(fips=fips)
            records = StateMortgageData.objects.filter(fips=fips)
            data = {
                "meta": {
                    "fips": fips,
                    "name": state.name,
                    "fips_type": "state",
                },
                "data": [record.time_series(days_late) for record in records],
            }
            return Response(data)
        if "non" in fips:
            records = NonMSAMortgageData.objects.filter(fips=fips)
            data = {
                "meta": {
                    "fips": fips,
                    "name": "Non-metro area of {}".format(
                        records.first().state.name
                    ),
                    "fips_type": "non_msa",
                },
                "data": [record.time_series(days_late) for record in records],
            }
            return Response(data)

        if fips in reference_lists["msa_fips"]:
            metro_area = MetroArea.objects.get(fips=fips, valid=True)
            records = MSAMortgageData.objects.filter(fips=fips)
            data = {
                "meta": {
                    "fips": fips,
                    "name": metro_area.name,
                    "fips_type": "msa",
                },
                "data": [record.time_series(days_late) for record in records],
            }
            return Response(data)
        else:  # must be a county request
            try:
                county = County.objects.get(fips=fips, valid=True)
            except County.DoesNotExist:
                return Response("County is below display threshold.")
            records = CountyMortgageData.objects.filter(fips=fips)
            name = "{}, {}".format(county.name, county.state.abbr)
            data = {
                "meta": {"fips": fips, "name": name, "fips_type": "county"},
                "data": [record.time_series(days_late) for record in records],
            }
        return Response(data)


def validate_year_month(year_month):
    """Trap non-integers, malformatted entries, and out-of-range dates."""

    current_year = datetime.date.today().year
    split = year_month.split("-")
    if len(split) != 2:
        return None
    try:
        year = int(split[0])
        month = int(split[1])
    except ValueError:
        return None
    if year > current_year or month not in range(1, 13):
        return None
    if year < 1998:
        return None
    return datetime.date(year, month, 1)


class MapData(APIView):
    """
    View for delivering geo-based map data by date
    from the mortgage performance dataset.
    """

    renderer_classes = (JSONRenderer,)

    def get(self, request, days_late, geo, year_month):
        date = validate_year_month(year_month)
        if date is None:
            return Response("Invalid year-month pair")
        if days_late not in DAYS_LATE_RANGE:
            return Response("Unknown delinquency range")
        geo_dict = {
            "national": {
                "queryset": NationalMortgageData.objects.get(date=date),
                "fips_type": "nation",
                "geo_obj": "",
            },
            "states": {
                "queryset": StateMortgageData.objects.filter(date=date),
                "fips_type": "state",
                "geo_obj": "state",
            },
            "counties": {
                "queryset": CountyMortgageData.objects.filter(
                    date=date, county__valid=True
                ),
                "fips_type": "county",
                "geo_obj": "county",
            },
            "metros": {
                "queryset": MSAMortgageData.objects.filter(date=date),
                "fips_type": "msa",
                "geo_obj": "msa",
            },
        }
        if geo not in geo_dict:
            return Response("Unkown geographic unit")
        nat_records = geo_dict["national"]["queryset"]
        nat_data_series = nat_records.time_series(days_late)
        if geo == "national":
            payload = {
                "meta": {
                    "fips_type": geo_dict[geo]["fips_type"],
                    "date": "{}".format(date),
                },
                "data": {},
            }
            nat_data_series.update({"name": "United States"})
            del nat_data_series["date"]
            payload["data"].update(nat_data_series)
        else:
            records = geo_dict[geo]["queryset"]
            payload = {
                "meta": {
                    "fips_type": geo_dict[geo]["fips_type"],
                    "date": "{}".format(date),
                    "national_average": nat_data_series["value"],
                },
                "data": {},
            }
            for record in records:
                data_series = record.time_series(days_late)
                geo_parent = getattr(record, geo_dict[geo]["geo_obj"])
                if geo == "counties":
                    name = "{}, {}".format(
                        geo_parent.name, geo_parent.state.abbr
                    )
                else:
                    name = geo_parent.name
                data_series.update({"name": name})
                del data_series["date"]
                payload["data"].update({record.fips: data_series})
            if geo == "metros":
                for metro in MetroArea.objects.filter(valid=False):
                    payload["data"][metro.fips]["value"] = None
                for record in NonMSAMortgageData.objects.filter(date=date):
                    non_data_series = record.time_series(days_late)
                    if record.state.non_msa_valid is False:
                        non_data_series["value"] = None
                    non_name = "Non-metro area of {}".format(record.state.name)
                    non_data_series.update({"name": non_name})
                    del non_data_series["date"]
                    payload["data"].update({record.fips: non_data_series})
        return Response(payload)
