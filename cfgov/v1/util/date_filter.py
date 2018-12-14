from datetime import date, datetime

from dateutil.relativedelta import relativedelta


# For more information on date formatting, see the python documentation here:
# https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

full_date_patterns = (
    '%m/%d/%Y',     # 10/25/2016, 9/1/2016
    '%m-%d-%Y',     # 10-25-2016, 9-1-2016
    '%m/%d/%y',     # 10/25/16, 9/1/16
    '%m-%d-%y',     # 10-25-16, 9-1-16
)

month_year_date_patterns = (
    '%m/%Y',        # 10/2016, 7/2017
    '%m-%Y',        # 10-2016, 7-2017
    '%m/%y',        # 10/16, 4/18
    '%m-%y',        # 10-16, 4-18
)

year_date_patterns = (
    '%Y',           # 2016
)


def end_of_time_period(user_input, generated_date):
    specificity = determine_date_specificity(user_input)
    if specificity == 'full':
        return generated_date
    elif specificity == 'month_year':
        return end_of_month(generated_date)
    elif specificity == 'year':
        return end_of_year(generated_date)
    else:
        return None


def end_of_year(input_date):
    year = input_date.year
    end_date = date(year, 12, 31)
    return end_date


def end_of_month(input_date):
    return input_date + relativedelta(day=31)


def determine_date_specificity(user_input):
    for pattern in full_date_patterns:
        maybe_date = date_from_pattern(user_input, pattern)
        if maybe_date is not None:
            return 'full'

    for pattern in month_year_date_patterns:
        maybe_date = date_from_pattern(user_input, pattern)
        if maybe_date is not None:
            return 'month_year'

    for pattern in year_date_patterns:
        maybe_date = date_from_pattern(user_input, pattern)
        if maybe_date is not None:
            return 'year'

    return None


def date_from_pattern(date_str, pattern):
    try:
        date = datetime.strptime(date_str, pattern).date()
        return date
    except (ValueError, TypeError):
        return None
