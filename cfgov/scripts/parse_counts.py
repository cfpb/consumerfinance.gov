# Temporary script that runs on  the Public Enforcement Counts CSV
# This will remain in place until our API wrapping the enforcement
# actions in Wagtail is complete

import csv
from datetime import datetime as dt


def make_row(*values):
    return [val.strip() for val in values]


def make_date(val):
    d = val.strip().split('/')
    if len(d[2]) == 2:
        d[2] = '20' + d[2]
    return int(dt(int(d[2]), int(d[0]), int(d[1])).timestamp() * 1000)


with open('./products.csv', 'r') as csv_file:
    split = csv.reader(csv_file, delimiter=',')
    header = next(split)
    isFirst = 1
    o_json = open('counts.json', 'w')
    o_json.write('[\n')
    with open('counts.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(make_row(header[0], header[1], 'Count', 'URL'))

        last_x = 0
        incr = 1000
        total = 1

        for fields in split:
            writer.writerow(
                make_row(fields[0], fields[1], str(total), fields[9])
            )
            if not isFirst:
                o_json.write(',\n')
            else:
                isFirst = 0

            name = fields[0].strip()
            date = make_date(fields[1])
            url = fields[9]

            if date == last_x:
                date += incr
                incr += 1000
            else:
                last_x = date
                incr = 1000

            o_json.write(
                '{{"x":{}, "y":{}, "name":"{}", "url":"{}"}}'
                .format(date, total, name, url))
            total += 1
        o_json.write('\n]')
        o_json.close()
