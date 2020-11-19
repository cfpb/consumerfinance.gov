import csv
from v1.models.learn_page import EnforcementActionPage, EnforcementActionInstitutionType

def add_data(data_file='./cfgov/scripts/pea_counts.csv'):
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        split = csv.reader(csv_file, delimiter=',')
        header = next(split)
        data = {}

        for fields in split:
            settled = fields[2].strip()
            institution_type = fields[3]
            url = fields[5]
            data[url] = [
                True if settled == 'Settled' else False,
                [t.strip() for t in institution_type.split(';')]
            ]

        for page in EnforcementActionPage.objects.all():
            if not page.live or page.has_unpublished_changes:
                continue

            url = 'https://www.consumerfinance.gov' + page.get_url()

            try:
                page.settled = data[url][0]
                page.institution_types.set([EnforcementActionInstitutionType(
                    institution_type=t
                ) for t in data[url][1]])

                page.save()
            except:
                print('No data for:', url)


def run():
    add_data()
