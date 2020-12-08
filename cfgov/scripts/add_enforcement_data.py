# Need court, institution type, docket number, tags(sp pop&prod), categories
# status is record type

import csv
from datetime import datetime as dt
from decimal import Decimal
from re import sub

from v1.models.learn_page import (
    EnforcementActionDisposition, EnforcementActionPage
)


def strip_fields(f, *args):
    return [f[i].strip() for i in args]


def make_date(d):
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


def run():
    add_counts()
    add_relief()

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

    for page in EnforcementActionPage.objects.all():
        if not page.live or page.has_unpublished_changes:
            continue

        url = 'https://www.consumerfinance.gov' + page.get_url()

        try:
            page.enforcement_disposition.set([
                EnforcementActionDisposition(**x) for x in rdata[url]
            ])

            page.save()
        except KeyError:
            print('No data for', url)
