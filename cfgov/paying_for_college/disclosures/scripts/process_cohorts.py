import datetime
import logging

import localflavor

from paying_for_college.models.disclosures import (
    DEFAULT_EXCLUSIONS,
    HIGHEST_DEGREES,
    School,
)


STATES = sorted(
    [tup[0] for tup in localflavor.us.us_states.CONTIGUOUS_STATES]
    + [tup[0] for tup in localflavor.us.us_states.NON_CONTIGUOUS_STATES]
    + ["PR"]
)
DEGREE_COHORTS = {k: [] for k in HIGHEST_DEGREES.keys()}
logger = logging.getLogger(__name__)


def get_grad_level(school):
    """Consider degrees higher than graduate level '4' as graduate degrees."""
    if int(school.degrees_highest) > 4:
        return "4"
    else:
        return school.degrees_highest


def build_base_cohorts():
    """
    Pre-build the base highest-degree cohorts.

    DEFAULT_EXCLUSIONS are the primary keys for the home offices of schools
    or school systems, plus our fake demo school, 999999.
    """
    global DEGREE_COHORTS
    base_query = (
        School.objects.filter(operating=True, state__in=STATES)
        .exclude(pk__in=DEFAULT_EXCLUSIONS)
        .exclude(degrees_highest="")
    )
    for key in DEGREE_COHORTS:
        DEGREE_COHORTS[key] += [
            school for school in base_query if get_grad_level(school) == key
        ]
    return base_query


def calculate_percentile_rank(array, score):
    """Get a school score's percentile rank from an array of cohort scores."""
    true_false_array = [value <= score for value in array]
    if len(true_false_array) == 0:
        return
    raw_rank = float(sum(true_false_array)) / len(true_false_array)
    return int(round(raw_rank * 100))


def rank_by_metric(school, cohort, metric):
    """Return a school's percentile rank among a cohort by 3 metrics."""
    values = [
        getattr(s, metric) for s in cohort if getattr(s, metric) is not None
    ]
    payload = {"cohort_count": len(values)}
    array = [float(val) for val in values]
    target_value = float(getattr(school, metric))
    payload.update(
        {"percentile_rank": calculate_percentile_rank(array, target_value)}
    )
    return payload


def run(single_school=None):
    """Get percentile rankings for schools by degree, control, and state."""
    count = 0
    starter = datetime.datetime.now()
    base_query = build_base_cohorts()
    if single_school:
        base_query = base_query.filter(pk=single_school)
    for school in base_query:
        by_degree = {}
        by_state = {}
        by_control = {}
        count += 1
        if count % 500 == 0:  # pragma: no cover
            logger.info("{} schools processed".format(count))
        # degree_cohort is the default, national base cohort
        # base query weeds out schools without state or degrees_highest values
        degree_cohort = DEGREE_COHORTS.get(get_grad_level(school))
        state_cohort = [
            s
            for s in degree_cohort
            if s and s.state and s.state == school.state
        ]
        # For school control, we want cohorts only for public and private;
        # We do not want a special cohort of for-profit schools
        if not school.control:
            control_cohort = None
        elif school.control == "Public":
            control_cohort = [
                s for s in degree_cohort if s.control == school.control
            ]
        else:
            control_cohort = [
                s for s in degree_cohort if s.control != "Public"
            ]
        for metric in ["grad_rate", "repay_3yr", "median_total_debt"]:
            if getattr(school, metric) is None:
                by_state.update({metric: None})
                by_control.update({metric: None})
                by_degree.update({metric: None})
            else:
                if state_cohort:
                    by_state.update(
                        {metric: rank_by_metric(school, state_cohort, metric)}
                    )
                if control_cohort:
                    by_control.update(
                        {
                            metric: rank_by_metric(
                                school, control_cohort, metric
                            )
                        }
                    )
                if degree_cohort:
                    by_degree.update(
                        {metric: rank_by_metric(school, degree_cohort, metric)}
                    )
        school.cohort_ranking_by_state = by_state
        school.cohort_ranking_by_control = by_control
        school.cohort_ranking_by_highest_degree = by_degree
        school.save()
    logger.info(
        "\nCohort script took {} to process {} schools".format(
            datetime.datetime.now() - starter, count
        )
    )
