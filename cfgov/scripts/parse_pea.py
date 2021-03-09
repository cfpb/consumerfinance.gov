# Temporary script that runs on  the Public Enforcement Actions CSV
# This will remain in place until our API wrapping the enforcement
# actions in Wagtail is complete

import csv
from datetime import datetime as dt


def make_row(row, *positions):
    return [row[pos].strip() for pos in positions]


def make_date(val):
    d = val.strip().split('/')
    if len(d[2]) == 2:
        d[2] = '20' + d[2]
    return int(dt(int(d[2]), int(d[0]), int(d[1])).timestamp() * 1000)


with open('./pea.csv', 'r', encoding='utf-8-sig') as csv_file:
    split = csv.reader(csv_file, delimiter=',')
    header = next(split)
    total = 0
    isFirst = 1
    o_json = open('relief.json', 'w')
    o_json.write('[\n')
    with open('relief.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([header[1], header[4], header[6], header[0], 'URL'])

        last_x = 0
        incr = 1000

        for fields in split:
            # skip rows with no final disposition
            if not fields[4]:
                continue

            writer.writerow(make_row(fields, 1, 4, 6, 0, 23))
            if not isFirst:
                o_json.write(',\n')
            else:
                isFirst = 0
            name = fields[1].strip()
            final = make_date(fields[4])
            relief = fields[6].strip().replace(',', '').replace('.', '')
            url = fields[23]
            if relief[0] == '$':
                relief = relief[1:]
            if relief == '-':
                relief = 0
            relief = int(relief)
            total += relief

            if final == last_x:
                final += incr
                incr += 1000
            else:
                last_x = final
                incr = 1000

            o_json.write(
                '{{"x":{},"y":{},"name":"{}","relief":"{:,.2f}","url":"{}"}}'
                .format(final, total / 100, name, relief / 100, url))
        o_json.write('\n]')
        o_json.close()
