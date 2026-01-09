import datetime
import logging


logger = logging.getLogger(__name__)
thru_date_map = {"03": "12", "06": "03", "09": "06", "12": "09"}


def get_thrudate(latest_file):
    """
    Use the latest filename to derive a through_date for processing.

    The source file ends with a MMYY date suffix that we can use.
    A typical source file name: delinquency_county_0625.csv

    We exclude the latest 3 months of data because the most recent
    reports are incomplete and can show misleading results. For that reason,
    the thru_date year needs to be pushed back a year for 03 data.
    """
    century = datetime.date.today().year // 100
    data_date_suffix = latest_file.rstrip(".csv")[-4:]
    data_month = data_date_suffix[:2]
    data_short_year = data_date_suffix[-2:]
    data_year = int(f"{century}{data_short_year}")
    thru_month = thru_date_map.get(data_month)
    if not thru_month:
        logger.error(
            f"Check the MMYY date suffix on the source file ({latest_file})\n"
            "The two-digit month value should be 03, 06, 09 or 12"
        )
        return
    thru_year = data_year - 1 if data_month == "03" else data_year
    thru_date = f"{thru_year}-{thru_month}-01"
    return thru_date
