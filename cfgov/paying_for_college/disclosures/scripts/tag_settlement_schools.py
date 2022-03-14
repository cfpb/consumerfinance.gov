from paying_for_college.disclosures.scripts.load_programs import read_in_s3
from paying_for_college.views import get_school


def tag_schools(s3_url):
    """
    Sets schools' 'settlement_school' value based on a CSV

    Assumes the CSV's headings include fields for 'ipeds_unit_id' and 'flag'
    """
    counter = 0
    csv_data = read_in_s3(s3_url)
    if not csv_data[0]:
        return "ERROR: could not read data from {0}".format(s3_url)
    headings = csv_data[0].keys()
    for heading in ["ipeds_unit_id", "flag"]:
        if heading not in headings:
            return (
                "ERROR: CSV doesn't have required fields; "
                "fields found were {}".format(headings)
            )
    initial_flag = csv_data[0]["flag"]
    for row in csv_data:
        school = None
        if row["ipeds_unit_id"]:
            school = get_school(row["ipeds_unit_id"])
        if school:
            school.settlement_school = row["flag"]
            school.save()
            counter += 1
    intro = "school was" if counter == 1 else "schools were"
    return "{} {} tagged as '{}' settlement schools".format(
        counter, intro, initial_flag
    )
