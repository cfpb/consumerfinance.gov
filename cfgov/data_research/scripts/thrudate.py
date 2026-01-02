import datetime
import logging


logger = logging.getLogger(__name__)
thru_date_map = {"03": "12", "06": "03", "09": "06", "12": "09"}


def get_thrudate(latest_file):
    """
    Use the latest filename to derive a through_date for processing.

    We exclude the latest 3 months of data because the most recent
    reports are incomplete and can show misleading results.
    The source file ends with a MMYY date suffix that we can use.
    A typical source file name: delinquency_county_0625.csv
    """
    this_year = datetime.date.today().year
    short_year = this_year % 100
    date_suffix = latest_file.rstrip(".csv")[-4:]
    latest_month = date_suffix[:2]
    latest_year = date_suffix[-2:]
    thru_month = thru_date_map.get(latest_month)
    if not thru_month:
        logger.error(
            f"Check the MMYY date suffix on the source file ({latest_file})\n"
            "The two-digit month value should be 03, 06, 09 or 12"
        )
        return
    if latest_year != f"{short_year}":
        logger.error(
            f"Check the MMYY date suffix on the source file ({latest_file})\n"
            f"The two-digit year value should be {short_year}"
        )
        return
    thru_year = this_year - 1 if thru_month == "12" else this_year
    thru_date = f"{thru_year}-{thru_month}-01"
    return thru_date
