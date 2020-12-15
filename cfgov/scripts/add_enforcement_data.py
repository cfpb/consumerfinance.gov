# This is a one time script used to populate enforcement actions
# across the site with data from our internal ENForce system
# Currently this data has been reported in two csvs, a relief
# csv and a count csv, with different pieces of data in each.
# Ideally all the data would be in one csv and would include
# court, institution type, docket number, special populations,
# products, and forum (none of which are included in either csv now).
# Once this final csv is produced, the code below will be modified
# to reload the complete dataset into the enforcement actions in wagtail
#
# To run this script, invoke it as follows:
# cfgov/manage.py runscript add_enforcement_data --script-args
#    [COUNT_CSV_PATH] [RELIEF_CSV_PATH]

import csv
import logging
import sys
from datetime import datetime as dt
from decimal import Decimal
from re import sub

from v1.models.learn_page import (
    EnforcementActionDisposition, EnforcementActionPage
)


logger = logging.getLogger(__name__)


def strip_fields(f, *args):
    return [f[i].strip() for i in args]


def make_date(d):
    d = sub('2020', '20', d)
    return dt.strptime(d, '%m/%d/%y') if d else ''


def money_to_dec(m):
    s = sub(r'[^\d.]', '', m) or 0
    return Decimal(s)


record_to_status = {
    'Final Order': 'post-order-post-judgment',
    'Dismissal': 'expired-terminated-dismissed',
    '': 'pending-litigation'
}

cdata = {}
rdata = {}


def add_relief(data_file='./cfgov/scripts/pea.csv'):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        # header
        next(split)

        for fields in split:
            (name,
             record_type,
             date_filed,
             final_order_date,
             dismissal_date,
             total_consumer_relief,
             civil_money_penalties,
             url) = strip_fields(fields, 1, 2, 3, 4, 5, 6, 17, 23)

            o = {
                'name': name,
                'status': record_to_status[record_type],
                'date_filed': make_date(date_filed),
                'final_order_date': make_date(final_order_date),
                'dismissal_date': make_date(dismissal_date),
                'total_consumer_relief': money_to_dec(total_consumer_relief),
                'civil_money_penalties': money_to_dec(civil_money_penalties)
            }

            try:
                rdata[url].append(o)
            except KeyError:
                rdata[url] = [o]


def add_counts(data_file='./cfgov/scripts/pea_counts.csv'):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        # header
        next(split)

        for fields in split:
            settled, institution_type, url = strip_fields(fields, 2, 3, 5)
            if 'Individual' in institution_type:
                it = 'Individual'
            elif 'Non-Bank' in institution_type:
                it = 'Non-Bank'
            else:
                it = 'Bank'
            o = {
                'settled': True if settled == 'Settled' else False,
                'institution_type': it
            }
            try:
                cdata[url].append(o)
            except KeyError:
                cdata[url] = [o]


def run(*args):
    if not args or len(args) != 2:
        logger.error("error. Use --script-args [COUNT_PATH] [RELIEF_PATH] " +
                     "to specify the location of the data csvs.")
        sys.exit()
    add_counts(args[0])
    add_relief(args[1])

    for url in rdata:
        for i in range(len(rdata[url])):
            if len(cdata[url]) > i:
                c_index = i
            else:
                c_index = 0
            curr_r = rdata[url][i]
            curr_c = cdata[url][c_index]
            curr_r['settled'] = curr_c['settled']
            curr_r['institution_type'] = curr_c['institution_type']

    for url in rdata:
        for disp in rdata[url]:
            to_del = []
            for key in disp:
                if disp[key] == '':
                    to_del.append(key)
            for key in to_del:
                del disp[key]

    count = 0

    for page in EnforcementActionPage.objects.all():
        if not page.live or page.has_unpublished_changes:
            logger.info(f"Skipping unpublished page: {page.slug}\n")
            continue

        url = 'https://www.consumerfinance.gov' + page.get_url()

        try:
            page.enforcement_dispositions.set([
                EnforcementActionDisposition(**x) for x in rdata[url]
            ])

            page.save()
            count += 1
        except KeyError:
            logger.info(f"No data in csv data file for {url}\n")

    logger.info(f"Data update finished. {count} pages updated.")
