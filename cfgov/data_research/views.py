from __future__ import unicode_literals
import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_csv import renderers as rfc_renderers

from data_research.models import (
    CountyMortgageData,
    # MortgageDataConstant,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta


class TimeSeriesNational(APIView):
    """
    View for delivering national time-series data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request):
        records = NationalMortgageData.objects.all()
        data = {'meta': {'name': 'United States',
                         'fips_type': 'national'},
                'data': [record.time_series for record in records]}
        return Response(data)


class TimeSeriesData(APIView):
    """
    View for delivering geo-based time-series data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , rfc_renderers.CSVRenderer)

    def get(self, request, fips):
        """
        Return a FIPS-based slice of base data as a json timeseries.
        """
        load_fips_meta()
        if fips not in FIPS.all_fips:
            return Response("FIPS code not found.")
        DATE_STARTER = datetime.date(FIPS.starting_year, 1, 1)
        if fips in FIPS.state_fips:
            records = StateMortgageData.objects.filter(
                fips=fips, date__gte=DATE_STARTER, valid=True)
            data = {'meta': {'fips': fips,
                             'name': FIPS.state_fips[fips]['name'],
                             'fips_type': 'state'},
                    'data': [record.time_series for record in records]}
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
                    'data': [record.time_series for record in records]}
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
                    'data': [record.time_series for record in records]}
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

    def get(self, request, geo, year_month):
        load_fips_meta()
        date = validate_year_month(year_month)
        if date is None:
            return Response("Invalid year-month pair")
        geo_dict = {
            'counties': {'queryset': CountyMortgageData.objects.filter(
                         date=date, valid=True),
                         'fips_type': 'county'},
            'metros': {'queryset': MSAMortgageData.objects.filter(
                       date=date, valid=True),
                       'fips_type': 'metro'},
            'states': {'queryset': StateMortgageData.objects.filter(
                       date=date, valid=True),
                       'fips_type': 'state'}
        }
        records = geo_dict[geo]['queryset']
        data = {'meta': {'fips_type': geo_dict[geo]['fips_type'],
                         'date': '{}'.format(date)},
                'data': {}}
        if geo == 'counties':
            data['data'].update(
                {record.fips: {'name': "{}, {}".format(
                    FIPS.county_fips[record.fips]['county'],
                    FIPS.county_fips[record.fips]['state']),
                    'pct30': record.time_series['pct30'],
                    'pct90': record.time_series['pct90']}
                 for record in records})
        elif geo == 'metros':
            data['data'].update(
                {record.fips:
                    {'name': FIPS.msa_fips[record.fips]['msa'],
                     'pct30': record.time_series['pct30'],
                     'pct90': record.time_series['pct90']}
                 for record in records})
        elif geo == 'states':
            data['data'].update(
                {record.fips:
                    {'name': FIPS.state_fips[record.fips]['name'],
                     'pct30': record.time_series['pct30'],
                     'pct90': record.time_series['pct90']}
                 for record in records})
        return Response(data)
