from __future__ import unicode_literals
import datetime

import json

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_csv import renderers as rfc_renderers

from data_research.models import (
    CountyMortgageData,
    # MortgageDataConstant,
    MSAMortgageData,
    MortgageMetaData,
    NationalMortgageData,
    StateMortgageData)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta

ALLOWED_DATE_RANGES = ['30-89', '90']


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
        meta_json = json.loads(record.json_value)
        return Response(meta_json)


class TimeSeriesNational(APIView):
    """
    View for delivering national time-series data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request, days_late):
        if days_late not in ALLOWED_DATE_RANGES:
            return Response("Unknown delinquency range")
        records = NationalMortgageData.objects.all()
        data = {'meta': {'name': 'United States',
                         'fips_type': 'national'},
                'data': [record.time_series(days_late)
                         for record in records]}
        return Response(data)


class TimeSeriesData(APIView):
    """
    View for delivering geo-based time-series data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request, days_late, fips):
        """
        Return a FIPS-based slice of base data as a json timeseries.
        """
        if days_late not in ALLOWED_DATE_RANGES:
            return Response("Unknown delinquency range")
        load_fips_meta()
        if fips not in FIPS.all_fips:
            return Response("FIPS code not found.")
        DATE_STARTER = datetime.date(FIPS.starting_year, 1, 1)
        if len(fips) == 2:
            records = StateMortgageData.objects.filter(
                fips=fips, date__gte=DATE_STARTER, valid=True)
            data = {'meta': {'fips': fips,
                             'name': FIPS.state_fips[fips]['name'],
                             'fips_type': 'state'},
                    'data': [record.time_series(days_late)
                             for record in records]}
            return Response(data)

        if fips in FIPS.msa_fips:
            records = MSAMortgageData.objects.filter(
                fips=fips, date__gte=DATE_STARTER, valid=True)
            if not records:
                return Response("Metro area is below display threshold.")
            name = FIPS.msa_fips[fips]['msa']
            data = {'meta': {'fips': fips,
                             'name': name,
                             'fips_type': 'msa'},
                    'data': [record.time_series(days_late)
                             for record in records]}
        else:
            records = CountyMortgageData.objects.filter(
                fips=fips, date__gte=DATE_STARTER, valid=True)
            if not records:
                return Response("County is below display threshold.")
            name = "{}, {}".format(
                FIPS.county_fips[fips]['county'],
                FIPS.county_fips[fips]['state'])
            data = {'meta': {'fips': fips,
                             'name': name,
                             'fips_type': 'county'},
                    'data': [record.time_series(days_late)
                             for record in records]}
        return Response(data)


def validate_year_month(year_month):
    """Trap non-integers, malformatted entries, and out-of-range dates."""

    current_year = datetime.date.today().year
    split = year_month.split('-')
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
    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request, geo, days_late, year_month):
        date = validate_year_month(year_month)
        if date is None:
            return Response("Invalid year-month pair")
        if days_late not in ALLOWED_DATE_RANGES:
            return Response("Unknown delinquency range")
        load_fips_meta()
        geo_dict = {
            'national':
                {'queryset': NationalMortgageData.objects.get(date=date),
                 'fips_type': 'nation',
                 'fips_meta': ''},
            'counties':
                {'queryset': CountyMortgageData.objects.filter(
                    date=date, valid=True),
                 'fips_type': 'county',
                 'fips_meta': FIPS.county_fips},
            'metros':
                {'queryset': MSAMortgageData.objects.filter(
                    date=date, valid=True),
                 'fips_type': 'metro',
                 'fips_meta': FIPS.msa_fips},
            'states':
                {'queryset': StateMortgageData.objects.filter(
                    date=date, valid=True),
                 'fips_type': 'state',
                 'fips_meta': FIPS.state_fips}
        }
        if geo not in geo_dict:
            return Response("Unkown geographic unit")
        nat_records = geo_dict['national']['queryset']
        nat_data_series = nat_records.time_series(days_late)
        if geo == 'national':
            payload = {'meta': {'fips_type': geo_dict[geo]['fips_type'],
                                'date': '{}'.format(date)},
                       'data': {}}
            nat_data_series.update({'name': 'United States'})
            payload['data'].update(nat_data_series)
        else:
            records = geo_dict[geo]['queryset']
            fips_meta = geo_dict[geo]['fips_meta']
            payload = {'meta': {'fips_type': geo_dict[geo]['fips_type'],
                                'date': '{}'.format(date),
                                'national_average': nat_data_series['value']},
                       'data': {}}
            for record in records:
                data_series = record.time_series(days_late)
                data_series.update(
                    {'name': fips_meta[record.fips]['name']})
                if geo == 'counties':
                    data_series['name'] += (
                        ', {}'.format(fips_meta[record.fips]['state']))
                payload['data'].update({record.fips: data_series})
        return Response(payload)
