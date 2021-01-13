# This is a one time script used to populate enforcement actions
# across the site with data from our internal ENForce system
# Currently this data has been reported in three csvs, a relief
# csv, a product csv, and a statute csv, with different pieces
# of data in each.
#
# In the future, data will be drawn from Wagtail itself instead
# of being loaded from these scattered csvs.
#
# To run this script, invoke it as follows:
# cfgov/manage.py runscript add_final_enforcement_data --script-args
#    [RELIEF_CSV_PATH] [PRODUCT_CSV_PATH] [STATUTE_CSV_PATH]

import csv
import logging
import sys
from datetime import datetime as dt
from decimal import Decimal
from re import sub

from django.core.exceptions import ValidationError

from v1.models.enforcement_action_page import (
    EnforcementActionAtRisk, EnforcementActionDefendantType,
    EnforcementActionDisposition, EnforcementActionDocket,
    EnforcementActionPage, EnforcementActionProduct, EnforcementActionStatute
)


logger = logging.getLogger(__name__)


def strip_fields(f, *args):
    return [f[i].strip() for i in args]


def make_date(d):
    d = sub('2020', '20', d)
    return dt.strptime(d, '%m/%d/%y') if d else ''


def make_money(tup_m):
    if tup_m[0] > 3 and tup_m[0] < 12:
        return money_to_dec(tup_m[1])
    else:
        return tup_m[1]


def money_to_dec(m):
    s = sub(r'[^\d.]', '', m) or 0
    return Decimal(s)


data = {}


def add_relief(data_file='./cfgov/scripts/pea.csv'):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        # header
        next(split)

        for fields in split:
            (
                name,
                record_type,
                final_order_date,
                dismissal_date,
                redress,
                redress_sus,
                o_relief,
                o_relief_sus,
                disgorgement,
                disgorgement_sus,
                cmp,
                cmp_sus,
                est_number,
                url
            ) = map(make_money, enumerate(strip_fields(
                fields, 1, 2, 4, 5, 9, 10, 12, 13, 15, 16, 17, 18, 20, 23
            )))

            o = {
                'final_disposition': name,
                'final_disposition_type': record_type,
                'final_order_consumer_redress': redress,
                'final_order_consumer_redress_suspended': redress_sus,
                'final_order_other_consumer_relief': o_relief,
                'final_order_other_consumer_relief_suspended': o_relief_sus,
                'final_order_disgorgement': disgorgement,
                'final_order_disgorgement_suspended': disgorgement_sus,
                'final_order_civil_money_penalty': cmp,
                'final_order_civil_money_penalty_suspended': cmp_sus,
                'estimated_consumers_entitled_to_relief': est_number
            }

            if final_order_date != '':
                o['final_order_date'] = make_date(final_order_date)
            if dismissal_date != '':
                o['dismissal_date'] = make_date(dismissal_date)

            try:
                data[url]['dispositions'].append(o)
            except KeyError:
                data[url] = {'dispositions': [o]}


def add_products(data_file):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        # header
        next(split)

        for fields in split:
            (
                name,
                initial_filing_date,
                defendant_type,
                court,
                docket,
                settled,
                products,
                at_risk_groups,
                url
            ) = strip_fields(fields, 0, 1, 2, 4, 5, 6, 7, 8, 9)

            defendant_type = [
                {'defendant_type': x}
                for x in defendant_type.split('; ') if x != ''
            ]

            docket = [
                {'docket_number': x} for x in docket.split('; ') if x != ''
            ]

            products = [
                {'product': x}
                for x in products.replace(' (Including Payday)', '').replace(
                    ' (Not Payday)', ''
                ).split('; ') if x != ''
            ]

            at_risk_groups = [
                {'at_risk_group': x}
                for x in at_risk_groups.split('; ') if x != ''
            ]

            try:
                data[url]['public_enforcement_action'] = name
                data[url]['initial_filing_date'] = make_date(
                    initial_filing_date
                )
                data[url]['defendant_types'] = defendant_type
                data[url]['court'] = court
                data[url]['docket_numbers'] = docket
                data[url]['settled_or_contested_at_filing'] = settled
                data[url]['products'] = products
                data[url]['at_risk_groups'] = at_risk_groups
            except KeyError:
                logger.info(f"No data in csv data file for {url}\n")


def add_statutes(data_file):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        # header
        next(split)

        provisions = ['Deceptive', 'Unfair', 'Abusive']

        o = {}

        for fields in split:
            (
                statute,
                provision,
                url
            ) = strip_fields(fields, 1, 2, 3)

            if statute == 'CFPA' and provision in provisions:
                statute = 'CFPA ' + provision

            try:
                o[url].append(statute)
            except KeyError:
                o[url] = [statute]

        for url in o:
            data[url]['statutes'] = [
                {'statute': x} for x in list(dict.fromkeys(o[url]))
            ]


def run(*args):
    if not args or len(args) != 3:
        logger.error("error. Use --script-args [RELIEF_PATH] " +
                     "[PRODUCT_PATH] [STATUTE_PATH] " +
                     "to specify the location of the data csvs.")
        sys.exit()
    add_relief(args[0])
    add_products(args[1])
    add_statutes(args[2])

    count = 0

    for page in EnforcementActionPage.objects.all():
        if not page.live or page.get_parent().title != 'Enforcement Actions':
            logger.info(f"Skipping unpublished page: {page.slug}\n")
            continue
        url = 'https://www.consumerfinance.gov' + page.get_url()

        try:
            page.public_enforcement_action = data[url][
                'public_enforcement_action'
            ]
            page.initial_filing_date = data[url]['initial_filing_date']
            page.court = data[url]['court']
            page.settled_or_contested_at_filing = data[url][
                'settled_or_contested_at_filing'
            ]

            page.enforcement_dispositions.set([
                EnforcementActionDisposition(**x)
                for x in data[url]['dispositions']
            ])
            page.defendant_types.set([
                EnforcementActionDefendantType(**x)
                for x in data[url]['defendant_types']
            ])
            page.docket_numbers.set([
                EnforcementActionDocket(**x)
                for x in data[url]['docket_numbers']
            ])
            page.products.set([
                EnforcementActionProduct(**x)
                for x in data[url]['products']
            ])
            page.at_risk_groups.set([
                EnforcementActionAtRisk(**x)
                for x in data[url]['at_risk_groups']
            ])
            page.statutes.set([
                EnforcementActionStatute(**x)
                for x in data[url]['statutes']
            ])

            try:
                def clean(model_list):
                    return (v.full_clean() for v in model_list)

                page.full_clean()
                clean(page.enforcement_dispositions.all())
                clean(page.defendant_types.all())
                clean(page.docket_numbers.all())
                clean(page.products.all())
                clean(page.at_risk_groups.all())
                clean(page.statutes.all())
                page.save()
                count += 1
            except ValidationError:
                logger.info(f"Field validation failed for {url}\n")

        except KeyError:
            logger.info(f"No data in csv data files for {url}\n")

    logger.info(f"Data update finished. {count} pages updated.")
