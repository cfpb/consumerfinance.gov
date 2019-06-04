from __future__ import unicode_literals

from paying_for_college.models import School, cdr


"""
# Data processing steps

This script was used to process an ed.gov xls file to identify perkins schools
- source: https://studentaid.ed.gov/sa/about/data-center/student/title-iv
- file: 2014-15CampusBased.xls, from the last dropdown: Campus-Based Volume

The xls was converted and sliced using csvkit and sed, following these steps:
- convert xls to csv
- delete the top 3 lines, which are fake headings
- Grab only the columns we're interested in: 1,2,9 which are
    - OPE ID
    - School
    - Recipients (Perkins)

    ```
    in2csv 2014-15CampusBased.xls > 2014-15CampusBased.csv
    sed -i -orig 1,3d 2014-15CampusBased.csv
    csvcut -c 1,2,9 2014-15CampusBased.csv > 2015_perkins.csv
    ```

To run from the script from the Django shell:

```
./manage.py shell
from paying_for_college.data_sources.perkins_processing import *
misses = tag_schools(CSVFILE)
```

This will make a dry run and print what's not working.
This turned up two OPE IDS that were tied to groupings of schools
  - CUNY
  - University of South Carolina

Running without the dry-run option will apply `offers_perkins` values

```
misses = tag_schools(CSVFILE, dry_run=False)
```

"""

CSVFILE = 'paying_for_college/data_sources/2015_perkins.csv'
ENDNOTE = (
    'processed {} entries, found {} offering Perkins, '
    'updated {} schools in our database')
DRY_ENDNOTE = ENDNOTE.replace('updated', 'would have updated')
MISSNOTE = "Couldn't find {} schools by ope8_id"


# csv fieldnames: 'OPE ID', 'School', 'Recipients'
def load_perkins_data(csvfile):
    with open(csvfile, 'r') as f:
        reader = cdr(f)
        return [row for row in reader]


def tag_schools(csvfile, dry_run=True):
    if dry_run:
        print("DRY RUN ...\nto update schools, run with 'dry_run=False'")
    processed = 0
    potentials = 0
    updated = 0
    misses = []
    data = load_perkins_data(csvfile)
    for row in data:
        processed += 1
        if row['Recipients']:
            potentials += 1
            targets = School.objects.filter(ope8_id=int(row['OPE ID']))
            if not targets:
                misses.append(row)
            else:
                for target in targets:
                    updated += 1
                    target.offers_perkins = True
                    if dry_run is False:
                        target.save()
    if dry_run:
        print(DRY_ENDNOTE.format(processed, potentials, updated))
    else:
        print(ENDNOTE.format(processed, potentials, updated))
    if misses:
        print(MISSNOTE.format(len(misses)))
        print("These schools were not found:")
        for entry in misses:
            print entry
    return misses
