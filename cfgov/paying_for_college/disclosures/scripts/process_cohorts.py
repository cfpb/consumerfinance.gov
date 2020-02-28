import datetime
import sys

import localflavor

from paying_for_college.models import (
    CONTROL_MAP, FAKE_SCHOOL_PK, HIGHEST_DEGREES, School
)


DEGREES_HIGHEST = {k: [] for k in HIGHEST_DEGREES.keys()}

STATES = sorted(
    [tup[0] for tup in localflavor.us.us_states.CONTIGUOUS_STATES] +
    [tup[0] for tup in localflavor.us.us_states.NON_CONTIGUOUS_STATES] +
    ['PR']
)

STATE = {state: [] for state in STATES}

CONTROL = {v: [] for v in CONTROL_MAP.values()}


def build_cohorts():
    """Pre-build cohort sets for efficient processing."""
    global CONTROL
    global DEGREES_HIGHEST
    global STATE
    base_query = School.objects.filter(
        operating=True, state__in=STATES).exclude(pk=FAKE_SCHOOL_PK)
    for key in DEGREES_HIGHEST:
        DEGREES_HIGHEST[key] += [
            school for school in base_query.filter(degrees_highest=key)
        ]
    for key in CONTROL:
        CONTROL[key] += [
            school for school in base_query.filter(control=key)
        ]
    for key in STATE:
        STATE[key] += [
            school for school in base_query.filter(state=key)
        ]
    return base_query


def calculate_percentile_rank(array, target):
    """
    Derive a target school's percentile rank from an array of cohort scores.
    """
    true_false_array = [value <= target for value in array]
    if len(true_false_array) == 0:
        return
    raw_rank = float(sum(true_false_array)) / len(true_false_array)
    return int(round(raw_rank * 100))


def rank_by_metric(school, cohort, metric):
    """
    Return a school's percentile rank among a cohort by 3 metrics.

    Possible cohorts are by state, by highest degree, or by control type.
    Possible metrics are grad rate, repayment rate, or median total debt.
    """
    values = [getattr(s, metric) for s in cohort if getattr(s, metric)]
    payload = {'cohort_count': len(values)}
    array = [float(val) for val in values]
    target_value = float(getattr(school, metric))
    payload.update({
        'percentile_rank': calculate_percentile_rank(array, target_value)
    })
    return payload


def run(single_school=None):
    """Get percentile rankings for schools by control, degree, and state."""
    count = 0
    starter = datetime.datetime.now()
    base_query = build_cohorts()
    if single_school:
        base_query = School.objects.filter(pk=single_school)
    for school in base_query:
        by_state = {}
        by_control = {}
        by_highest_degree = {}
        count += 1
        if count % 500 == 0:  # pragma: no cover
            print(count)
        state_cohort = STATE.get(school.state) if school.state else None
        control_cohort = CONTROL.get(
            school.control) if school.control else None
        degree_cohort = DEGREES_HIGHEST.get(
            school.degrees_highest) if school.degrees_highest else None
        for metric in ['grad_rate', 'repay_3yr', 'median_total_debt']:
            if not getattr(school, metric):
                by_state.update({metric: None})
                by_control.update({metric: None})
                by_highest_degree.update({metric: None})
            else:
                if state_cohort:
                    by_state.update({
                        metric: rank_by_metric(school, state_cohort, metric)
                    })
                if control_cohort:
                    by_control.update({
                        metric: rank_by_metric(school, control_cohort, metric)
                    })
                if degree_cohort:
                    by_highest_degree.update({
                        metric: rank_by_metric(school, degree_cohort, metric)
                    })
        school.cohort_ranking_by_state = by_state
        school.cohort_ranking_by_control = by_control
        school.cohort_ranking_by_highest_degree = by_highest_degree
        school.save()
        sys.stdout.write('.')
        sys.stdout.flush()
    print("\ncohorts took {} to process {} schools".format(
        datetime.datetime.now() - starter,
        count
    ))
