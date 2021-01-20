import csv
import json
from datetime import datetime as dt
from re import sub

from v1.models.enforcement_action_page import (
    enforcement_at_risk_groups, enforcement_defendant_types,
    enforcement_products, enforcement_statutes
)


def strip_fields(f, *args):
    return [f[i].strip() for i in args]


def make_row(*values):
    return [val.strip() for val in values]


def make_date(val):
    d = val.strip().split('/')
    if len(d[2]) == 2:
        d[2] = '20' + d[2]
    return int(dt(int(d[2]), int(d[0]), int(d[1])).timestamp() * 1000)


def make_money(tup_m):
    if tup_m[0] > 3 and tup_m[0] < 12:
        return money_to_dec(tup_m[1])
    else:
        return tup_m[1]


def money_to_dec(m):
    s = sub(r'[^\d.]', '', m) or 0
    return float(s)


def match_list(li, match):
    for v in li:
        if v[0] == match:
            return v[1]
    print(li, match)
    raise


data = {}


def run(*args):
    with open('./scripts/products.csv', 'r') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        next(split)

        with open('counts.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                make_row(
                    'Public Enforcement Action', 'Initial Filing Date',
                    'Count', 'URL'
                )
            )

            total = 1

            for fields in split:
                writer.writerow(
                    make_row(fields[0], fields[1], str(total), fields[9])
                )

                total += 1

                name = fields[0].strip()
                date = make_date(fields[1])
                defendant_types = [
                    match_list(enforcement_defendant_types, f)
                    for f in fields[2].strip().split('; ') if f != ''
                ]
                court = fields[4].strip()
                docket_numbers = [fields[5].strip()]
                settled = fields[6].strip()
                products = [
                    match_list(enforcement_products, f)
                    for f in fields[7].strip().replace(
                        ' (Including Payday)', ''
                    ).replace(' (Not Payday)', '').split('; ') if f != ''
                ]
                at_risk_groups = [
                    match_list(enforcement_at_risk_groups, f)
                    for f in fields[8].strip().split('; ') if f != ''
                ]
                url = fields[9]

                data[url] = {
                    'public_enforcement_action': name,
                    'initial_filing_date': date,
                    'defendant_types': defendant_types,
                    'court': court,
                    'docket_numbers': docket_numbers,
                    'settled_or_contested_at_filing': settled,
                    'products': products,
                    'at_risk_groups': at_risk_groups
                }

    with open('./scripts/statutes.csv', 'r') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        next(split)

        provisions = ['Deceptive', 'Unfair', 'Abusive']

        for fields in split:
            statute = fields[1].strip()
            provision = fields[2].strip()
            url = fields[3].strip()

            if statute == 'CFPA' and provision in provisions:
                statute = 'CFPA ' + provision

            s = match_list(enforcement_statutes, statute)

            try:
                data[url]['statutes'].append(s)
            except KeyError:
                data[url]['statutes'] = [s]

    with open('./scripts/pea.csv', 'r') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        head = next(split)

        with open('relief.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([head[1], head[4], head[6], head[0], 'URL'])

            for fields in split:
                (
                    name,
                    record_type,
                    final_order_date,
                    dismissal_date,
                    redress,
                    redress_sus,
                    o_relief,
                    o_rel_sus,
                    disgorgement,
                    disgorgement_sus,
                    cmp,
                    cmp_sus,
                    est_number,
                    url
                ) = map(make_money, enumerate(strip_fields(
                    fields, 1, 2, 4, 5, 9, 10, 12, 13, 15, 16, 17, 18, 20, 23
                )))

                writer.writerow(make_row(
                    fields[1], fields[4], fields[6], fields[0], fields[23]
                ))

                o = {
                    'final_disposition': name,
                    'final_disposition_type': record_type,
                    'final_order_consumer_redress': redress,
                    'final_order_consumer_redress_suspended': redress_sus,
                    'final_order_other_consumer_relief': o_relief,
                    'final_order_other_consumer_relief_suspended': o_rel_sus,
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
                    data[url]['dispositions'] = [o]

    def ifd_sort(v):
        return v['initial_filing_date']

    list_data = []
    for key, val in data.items():
        val['url'] = key
        list_data.append(val)

    list_data.sort(reverse=True, key=ifd_sort)

    with open('./scripts/chart_data.json', 'w') as f:
        f.write(json.dumps(list_data))
