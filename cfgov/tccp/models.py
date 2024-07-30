import re
from functools import partial
from itertools import chain, product

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Case, Count, F, Max, Min, Q, Value, When
from django.db.models.functions import Coalesce

from dateutil.relativedelta import relativedelta
from tailslide import Percentile

from . import enums
from .fields import CurrencyDecimalField, JSONListField, YesNoBooleanField


REPORT_DATE_REGEX = re.compile(r"Data as of (\w+ \d+)")


Percentile25 = partial(Percentile, percentile=0.25)
Percentile75 = partial(Percentile, percentile=0.75)


class CardSurveyDataQuerySet(models.QuerySet):
    def available_in(self, value):
        """Filter cards by geographic availability.

        A value of None filters to cards that are available nationally.
        Any other value filters by that particular state.
        """
        q = Q(availability_of_credit_card_plan="National")

        if value is not None:
            q |= (
                Q(availability_of_credit_card_plan="One State/Territory")
                & Q(state=value)
            ) | (
                Q(availability_of_credit_card_plan="Regional")
                & Q(state_multiple__contains=value)
            )

        return self.filter(q)

    def invalid_aprs_q(self):
        """Selector to identify cards with invalid APR relationships.

        This selector includes cards that meet any of these criteria:

        1. {purchase, transfer}_apr_great > {purchase, transfer}_apr_good
        2. {purchase, transfer}_apr_good > {purchase, transfer}_apr_poor
        3. {purchase, transfer}_apr_great > {purchase, transfer}_apr_poor
        4. {purchase, transfer}_median > {purchase, transfer}_max
        5. {purchase, transfer}_min > {purchase, transfer}_max
        6. {purchase, transfer}_min > {purchase, transfer}_median
        """
        q = Q()

        for apr in ("purchase_apr", "transfer_apr"):
            for left, right in [
                ("great", "good"),
                ("good", "poor"),
                ("great", "poor"),
                ("median", "max"),
                ("min", "max"),
                ("min", "median"),
            ]:
                q |= Q(**{f"{apr}_{left}__gt": F(f"{apr}_{right}")})

        return q

    def exclude_invalid_aprs(self):
        return self.exclude(self.invalid_aprs_q())

    def only_invalid_aprs(self):
        return self.filter(self.invalid_aprs_q())

    def get_summary_statistics(self):
        """Compute aggregate purchase APR statistics for each credit tier."""

        # These are the statistics we want to compute:
        # (
        #  stat name,
        #  computation function,
        #  whether to include min/max-only cards in the computation (see below)
        # )
        stats = [
            ("count", Count, True),
            ("min", Min, True),
            ("max", Max, True),
            ("pct25", Percentile25, False),
            ("pct75", Percentile75, False),
        ]

        # Note that we only include a card in a certain tier if it both has a
        # valid APR for that tier AND if its "targeted_credit_tiers" column
        # includes the tier in its value. It's not enough that a card offers an
        # APR to the tier; it also has to be "targeted" to that tier.
        #
        # First we want to compute the 25th and 75th percentiles over all card
        # purchase APRs in a tier. To do this we need to identify a single
        # purchase APR value to use for each card. The logic for choosing this
        # single purchase APR works as follows, using the good tier as an
        # example:
        #
        # 1. If the "targeted_credit_tiers" column doesn't include the good
        #    tier, assign the card a purchase APR of None, which excludes it
        #    from percentile calculations.
        # 2. Otherwise, if the column "purchase_apr_good" is defined, use it
        #    as the card's purchase APR for percentile computations.
        # 3. Otherwise, if the column "purchase_apr_median" is defined, use it
        #    as the card's purchase APR for percentile computations.
        # 4. Otherwise, use an APR of None, which excludes the card from
        #    percentile calculations.
        #
        # This logic can be represented in SQL roughly as follows to aggregate
        # the purchase_apr_good_pct25 statistic:
        #
        # SELECT
        #   PERCENTILE_CONT(0.25)
        #   WITHIN GROUP (
        #     ORDER BY CASE
        #       WHEN
        #         targeted_credit_tiers" @> ["Credit scores from 620 to 719"]
        #       THEN
        #         COALESCE(
        #           purchase_apr_good,
        #           purchase_apr_median
        #         )
        #       ELSE NULL
        #     END
        #   ) AS purchase_apr_good_pct25
        # FROM ...
        #
        # Note that we deliberately do not use the global (non-tier-specific)
        # "purchase_apr_min" or "purchase_apr_max" columns when computing APR
        # percentiles. This excludes cards that lack median purchase APR values
        # but do provide a min/max pair.
        #
        # We also want to count how many cards are in each tier, which we can
        # do at the same time. This is equivalent to counting how many cards
        # have a non-null purchase APR for that tier. We can use the same logic
        # as above, with one exception: here we do want to include cards that
        # lack median APR values and have only a min/max pair. We do this by
        # adding an additional step to the logic, using the good tier as an
        # example:
        #
        # 1. If the "targeted_credit_tiers" column doesn't include the good
        #    tier, exclude this card from the count.
        # 2. Otherwise, if the column "purchase_apr_good" is defined, include
        #    this card in the count.
        # 3. Otherwise, if the column "purchase_apr_median" is defined, include
        #    this card in the count.
        # 4. Otherwise, if both columns "purchase_apr_min" and
        #    "purchase_apr_max" are defined, include this card in the count.
        # 4. Otherwise, exclude this card from the count.
        #
        # This logic can be represented in SQL roughly as follows to aggregate
        # the purchase_apr_good_count statistic:
        #
        # SELECT
        #   COUNT(
        #     CASE
        #       WHEN
        #         targeted_credit_tiers" @> ["Credit scores from 620 to 719"]
        #       THEN
        #         COALESCE(
        #           purchase_apr_good,
        #           purchase_apr_median,
        #           CASE
        #             WHEN
        #               purchase_apr_min IS NOT NULL AND
        #               purchase_apr_max IS NOT NULL
        #             THEN
        #               purchase_apr_max
        #             ELSE NULL
        #           END
        #         )
        #       ELSE NULL
        #     END
        #   ) AS purchase_apr_good_count
        # FROM ...
        #
        # Both the percentile and count logic is expressed in Django code here:
        aggregates = {
            f"purchase_apr_{tier_suffix}_{stat_name}": stat_fn(
                Case(
                    When(
                        targeted_credit_tiers__contains=tier_value,
                        then=Coalesce(
                            *(
                                [
                                    F(f"purchase_apr_{tier_suffix}"),
                                    F("purchase_apr_median"),
                                ]
                                + (
                                    [
                                        Case(
                                            When(
                                                Q(
                                                    purchase_apr_min__isnull=False
                                                )
                                                & Q(
                                                    purchase_apr_max__isnull=False
                                                ),
                                                then=F(
                                                    "purchase_apr_"
                                                    + ["max", "min"][
                                                        stat_name == "min"
                                                    ]
                                                ),
                                            ),
                                        )
                                    ]
                                    if include_min_max_only
                                    else []
                                )
                            )
                        ),
                    ),
                )
            )
            for (stat_name, stat_fn, include_min_max_only), (
                tier_value,
                tier_suffix,
            ) in product(stats, enums.CreditTierColumns)
        }

        aggregates.update(
            {
                "count": Count("pk"),
                "first_report_date": Min("report_date"),
            }
        )

        stats = self.aggregate(**dict(aggregates))

        # Manually add a statistic for the start of the reporting period,
        # which is assumed to be six months before the first report date.
        # Report dates are always at the end of the month.
        report_period_start = None
        if first_report_date := stats["first_report_date"]:
            report_period_start = (
                first_report_date
                + relativedelta(days=1)
                - relativedelta(months=6)
            )

        stats["report_period_start"] = report_period_start

        return stats

    def with_ratings(self, summary_stats=None):
        # Assign each card with a numeric rating based on its purchase APR."""
        qs = self

        # Card ratings are based on how a card's purchase APR relates to the
        # distribution of purchase APRs across other cards for that credit
        # tier. This computation relies on summary statistics for the entire
        # card dataset. If we haven't previously computed those stats, we need
        # to do so now.
        summary_stats = summary_stats or qs.get_summary_statistics()

        # For each card, we annotate twelve additional columns:
        #
        # {purchase, transfer}_apr_{poor, good, great}_{min, max}
        #
        # We want to select the most appropriate min and max APR to use for
        # both purchase APR and transfer APR for each of the three credit
        # tiers: poor, good, and great. We need APRs for each of these so that
        # we can both sort cards by APR (purchase or transfer) and also rate
        # cards by APR (purchase only, see code further down below). Most of
        # the time the min and the max APR for each of these combination will
        # end up being the same.
        #
        # The logic for APR selection works the same way as the count logic in
        # get_summary_statistics above. Using purchase APR for the good tier as
        # an example:
        #
        # 1. If the "targeted_credit_tiers" column doesn't include the good
        #    tier, assign the card min and max good purchase APRs of None.
        # 2. Otherwise, if the column "purchase_apr_good" is defined, use it
        #    for both the min and max good purchase APRs.
        # 3. Otherwise, if the column "purchase_apr_median" is defined, use it
        #    for both the min and max good purchase APRs.
        # 4. Otherwise, if both columns "purchase_apr_min" and
        #    "purchase_apr_max" are defined, use them as the min and max
        #    good purchase APRs.
        # 5. Otherwise, assign the card good min and max purchase APRs of None.
        #
        # This logic can be represented in SQL roughly as follows to annotate
        # the purchase_apr_good_min column:
        #
        # SELECT
        #   CASE
        #     WHEN
        #       targeted_credit_tiers @> ["Credit scores from 620 to 719"]
        #     THEN
        #       COALESCE(
        #         purchase_apr_good,
        #         purchase_apr_median,
        #         CASE
        #           WHEN
        #             purchase_apr_min IS NOT NULL AND
        #             purchase_apr_max IS NOT NULL
        #           THEN
        #             purchase_apr_min
        #           ELSE NULL
        #         END
        #       )
        #     ELSE NULL
        #   END AS purchase_apr_good_min
        # FROM ...
        #
        # This logic is expressed in Django code here:
        qs = qs.annotate(
            **{
                f"{apr}_apr_{tier_suffix}_{min_or_max}": Case(
                    When(
                        targeted_credit_tiers__contains=tier_value,
                        then=Coalesce(
                            F(f"{apr}_apr_{tier_suffix}"),
                            F(f"{apr}_apr_median"),
                            Case(
                                When(
                                    Q(**{f"{apr}_apr_min__isnull": False})
                                    & Q(**{f"{apr}_apr_max__isnull": False}),
                                    then=F(f"{apr}_apr_{min_or_max}"),
                                ),
                            ),
                        ),
                    ),
                    output_field=models.FloatField(),
                )
                for apr, (
                    tier_value,
                    tier_suffix,
                ), min_or_max in product(
                    ("purchase", "transfer"),
                    enums.CreditTierColumns,
                    ("min", "max"),
                )
            }
        )

        # We additionally annotate these three columns:
        #
        # purchase_apr_{poor, good, great}_rating
        #
        # These are computed by comparing the three maximum purchase APR
        # columns added above (purchase_apr_{poor, good, great}_max) with the
        # tier-specific percentiles passed in (or computed) above. Ratings are
        # assigned as:
        #
        #   purchase APR < 25th percentile: 0
        #   purchase APR < 75th percentile: 1
        #   purchase APR >= 75th percentile: 2
        #   null purchase APR: null
        #
        # This logic can be represented in SQL roughly as:
        #
        # SELECT
        #   CASE
        #     WHEN
        #       purchase_apr_good_max < purchase_apr_good_pct25
        #     THEN
        #       0
        #     WHEN
        #       purchase_apr_good_max < purchase_apr_good_pct75
        #     THEN
        #       1
        #     WHEN
        #       purchase_apr_good_max < purchase_apr_good_max
        #     THEN
        #       2
        #     ELSE NULL
        #   END AS purchase_apr_good_rating
        # FROM ...
        #
        # This logic is expressed in Django code here:
        #
        # (The "or 0"s below are necessary because it's possible that the
        # percentile might have been computed as None, if there are no cards
        # for this tier. This won't happen with real datasets but could happen
        # when testing this code with empty or minimal datasets.)
        qs = qs.annotate(
            **{
                f"purchase_apr_{tier_suffix}_rating": Case(
                    When(
                        **{
                            f"purchase_apr_{tier_suffix}_max__lt": summary_stats[  # noqa: E501
                                f"purchase_apr_{tier_suffix}_pct25"
                            ]
                            or 0
                        },
                        then=Value(0),
                    ),
                    When(
                        **{
                            f"purchase_apr_{tier_suffix}_max__lt": summary_stats[  # noqa: E501
                                f"purchase_apr_{tier_suffix}_pct75"
                            ]
                            or 0
                        },
                        then=Value(1),
                    ),
                    When(
                        **{f"purchase_apr_{tier_suffix}_max__isnull": False},
                        then=Value(2),
                    ),
                    output_field=models.IntegerField(),
                )
                for tier_suffix in dict(enums.CreditTierColumns).values()
            }
        )

        return qs

    def for_credit_tier(self, credit_tier):
        qs = self

        # Use the specified credit tier to annotate 5 new columns which can be
        # used downstream regardless of which tier we are filtering on:
        #
        # purchase_apr_for_tier_rating
        # {purchase, transfer}_apr_for_tier_{min, max}
        #
        # These columns are annotated as aliases of tier-specific columns which
        # we previously annotated. For example, if filtering for credit tier
        # "good", we can use columns:
        #
        # purchase_apr_good_rating
        # {purchase, transfer}_apr_good_{min, max}
        tier_suffix = dict(enums.CreditTierColumns)[credit_tier]

        qs = qs.annotate(
            purchase_apr_for_tier_rating=F(
                f"purchase_apr_{tier_suffix}_rating"
            ),
            **{
                f"{basename}_apr_for_tier_{min_or_max}": F(
                    f"{basename}_apr_{tier_suffix}_{min_or_max}"
                )
                for basename, min_or_max in product(
                    ("purchase", "transfer"), ("min", "max")
                )
            },
        )

        # If filtering by a credit tier, we also exclude cards for which we
        # weren't able to provide a purchase APR for that tier.
        qs = qs.exclude(purchase_apr_for_tier_min__isnull=True)

        return qs


class CardSurveyData(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True)
    institution_name = models.TextField()
    institution_type = models.TextField(
        choices=enums.InstitutionTypeChoices, null=True, blank=True
    )
    product_name = models.TextField(db_index=True)
    report_date = models.DateField()
    availability_of_credit_card_plan = models.TextField(
        choices=enums.GeoAvailabilityChoices
    )
    state = models.TextField(choices=enums.StateChoices, null=True, blank=True)
    state_multiple = JSONListField(choices=enums.StateChoices, blank=True)
    pertains_to_specific_counties = YesNoBooleanField(null=True, blank=True)
    requirements_for_opening = YesNoBooleanField()
    requirements_for_opening_types = JSONListField(
        choices=enums.RequirementsForOpeningChoices, blank=True
    )
    geographic_restrictions = models.TextField(null=True, blank=True)
    professional_affiliation = models.TextField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    secured_card = YesNoBooleanField()
    targeted_credit_tiers = JSONListField(choices=enums.CreditTierChoices)
    purchase_apr_offered = YesNoBooleanField()
    purchase_apr_vary_by_balance = YesNoBooleanField(null=True, blank=True)
    purchase_apr_balance_tier_1 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_1_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_1_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_2 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_2_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_2_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_3 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_3_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_3_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_4 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_4_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_4_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_index = YesNoBooleanField(null=True, blank=True)
    variable_rate_index = JSONListField(choices=enums.IndexChoices, blank=True)
    index = JSONListField(
        choices=enums.IndexTypeChoices, null=True, blank=True
    )
    purchase_apr_vary_by_credit_tier = YesNoBooleanField(null=True, blank=True)
    purchase_apr_no_score = models.FloatField(
        null=True, blank=True, db_index=True
    )
    purchase_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    purchase_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    purchase_apr_great = models.FloatField(
        null=True, blank=True, db_index=True
    )
    purchase_apr_min = models.FloatField(null=True, blank=True)
    purchase_apr_median = models.FloatField(null=True, blank=True)
    purchase_apr_max = models.FloatField(null=True, blank=True)
    introductory_apr_offered = YesNoBooleanField()
    introductory_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    intro_apr_no_score = models.FloatField(
        null=True, blank=True, db_index=True
    )
    intro_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_great = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_min = models.FloatField(null=True, blank=True)
    intro_apr_median = models.FloatField(null=True, blank=True)
    intro_apr_max = models.FloatField(null=True, blank=True)
    median_length_of_introductory_apr = models.FloatField(
        null=True, blank=True
    )
    balance_transfer_offered = YesNoBooleanField()
    balance_transfer_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    transfer_apr_no_score = models.FloatField(
        null=True, blank=True, db_index=True
    )
    transfer_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    transfer_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    transfer_apr_great = models.FloatField(
        null=True, blank=True, db_index=True
    )
    transfer_apr_min = models.FloatField(null=True, blank=True)
    transfer_apr_median = models.FloatField(null=True, blank=True)
    transfer_apr_max = models.FloatField(null=True, blank=True)
    median_length_of_balance_transfer_apr = models.FloatField(
        null=True, blank=True
    )
    balance_transfer_grace_period = YesNoBooleanField(null=True, blank=True)
    cash_advance_apr_offered = YesNoBooleanField()
    cash_advance_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    advance_apr_no_score = models.FloatField(
        null=True, blank=True, db_index=True
    )
    advance_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_great = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_min = models.FloatField(null=True, blank=True)
    advance_apr_median = models.FloatField(null=True, blank=True)
    advance_apr_max = models.FloatField(null=True, blank=True)
    grace_period_offered = YesNoBooleanField()
    grace_period = models.PositiveIntegerField(null=True, blank=True)
    minimum_finance_charge = YesNoBooleanField()
    minimum_finance_charge_dollars = CurrencyDecimalField(
        null=True, blank=True
    )
    balance_computation_method = JSONListField(
        choices=enums.BalanceComputationChoices
    )
    balance_computation_method_details = models.TextField(
        null=True, blank=True
    )
    periodic_fee_type = JSONListField(
        choices=enums.PeriodicFeeTypeChoices, blank=True
    )
    annual_fee = CurrencyDecimalField(null=True, blank=True)
    monthly_fee = CurrencyDecimalField(null=True, blank=True)
    weekly_fee = CurrencyDecimalField(null=True, blank=True)
    other_periodic_fee_name = models.TextField(null=True, blank=True)
    other_periodic_fee_amount = CurrencyDecimalField(null=True, blank=True)
    other_periodic_fee_frequency = models.TextField(null=True, blank=True)
    fee_varies = YesNoBooleanField(null=True, blank=True)
    periodic_min = CurrencyDecimalField(null=True, blank=True)
    periodic_max = CurrencyDecimalField(null=True, blank=True)
    fee_explanation = models.TextField(null=True, blank=True)
    purchase_transaction_fees = YesNoBooleanField()
    purchase_transaction_fee_type = JSONListField(
        choices=enums.PurchaseTransactionFeeTypeChoices, blank=True
    )
    purchase_transaction_fee_dollars = CurrencyDecimalField(
        null=True, blank=True
    )
    purchase_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_purchase_transaction_fee_amount = CurrencyDecimalField(
        null=True, blank=True
    )
    purchase_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    balance_transfer_fees = YesNoBooleanField(db_index=True)
    balance_transfer_fee_types = JSONListField(
        choices=enums.BalanceTransferFeeTypeChoices, blank=True
    )
    balance_transfer_fee_dollars = CurrencyDecimalField(null=True, blank=True)
    balance_transfer_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_balance_transfer_fee_amount = CurrencyDecimalField(
        null=True, blank=True
    )
    balance_transfer_fee_calculation = models.TextField(null=True, blank=True)
    cash_advance_fees = YesNoBooleanField()
    cash_advance_fee_for_each_transaction = YesNoBooleanField(
        null=True, blank=True
    )
    cash_advance_fee_types = JSONListField(
        choices=enums.CashAdvanceFeeTypeChoices, blank=True
    )
    cash_advance_fee_dollars = CurrencyDecimalField(null=True, blank=True)
    cash_advance_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_cash_advance_fee_amount = CurrencyDecimalField(
        null=True, blank=True
    )
    cash_advance_fee_calculation = models.TextField(null=True, blank=True)
    foreign_transaction_fees = YesNoBooleanField()
    foreign_transaction_fees_types = JSONListField(
        choices=enums.ForeignTransactionFeeTypeChoices, blank=True
    )
    foreign_transaction_fee_dollars = CurrencyDecimalField(
        null=True, blank=True
    )
    foreign_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_foreign_transaction_fee_amount = CurrencyDecimalField(
        null=True, blank=True
    )
    foreign_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    late_fees = YesNoBooleanField()
    late_fee_types = JSONListField(
        choices=enums.LateFeeTypeChoices, blank=True
    )
    late_fee_dollars = CurrencyDecimalField(null=True, blank=True)
    late_fee_six_month_billing_cycle = CurrencyDecimalField(
        null=True, blank=True
    )
    late_fee_policy_details = models.TextField(null=True, blank=True)
    fee_varies36 = YesNoBooleanField(null=True, blank=True)
    minimum37 = CurrencyDecimalField(null=True, blank=True)
    maximum38 = CurrencyDecimalField(null=True, blank=True)
    fee_explanation39 = models.TextField(null=True, blank=True)
    over_limit_fees = YesNoBooleanField()
    over_limit_fee_types = JSONListField(
        choices=enums.OverlimitFeeTypeChoices, blank=True
    )
    over_limit_fee_dollars = CurrencyDecimalField(null=True, blank=True)
    overlimit_fee_detail = models.TextField(null=True, blank=True)
    other_fees = YesNoBooleanField()
    additional_fees = YesNoBooleanField(null=True, blank=True)
    other_fee_name = models.TextField(null=True, blank=True)
    other_fee_amount = CurrencyDecimalField(null=True, blank=True)
    other_fee_explanation = models.TextField(null=True, blank=True)
    other_fee_name_2 = models.TextField(null=True, blank=True)
    other_fee_amount_2 = CurrencyDecimalField(null=True, blank=True)
    other_fee_explanation_2 = models.TextField(null=True, blank=True)
    other_fee_name_3 = models.TextField(null=True, blank=True)
    other_fee_amount_3 = CurrencyDecimalField(null=True, blank=True)
    other_fee_explanation_3 = models.TextField(null=True, blank=True)
    other_fee_name_4 = models.TextField(null=True, blank=True)
    other_fee_amount_4 = CurrencyDecimalField(null=True, blank=True)
    other_fee_explanation_4 = models.TextField(null=True, blank=True)
    other_fee_name_5 = models.TextField(null=True, blank=True)
    other_fee_amount_5 = CurrencyDecimalField(null=True, blank=True)
    other_fee_explanation_5 = models.TextField(null=True, blank=True)
    fee_varies56 = YesNoBooleanField(null=True, blank=True)
    minimum57 = CurrencyDecimalField(null=True, blank=True)
    maximum58 = CurrencyDecimalField(null=True, blank=True)
    fee_explanation59 = models.TextField(null=True, blank=True)
    services = JSONListField(choices=enums.ServicesChoices, blank=True)
    other_services = models.TextField(null=True, blank=True)
    rewards = JSONListField(choices=enums.RewardsChoices, blank=True)
    other_rewards = models.TextField(null=True, blank=True)
    card_features = JSONListField(choices=enums.FeaturesChoices, blank=True)
    other_card_features = models.TextField(null=True, blank=True)
    contact_information_types = JSONListField(
        choices=enums.ContactTypeChoices, blank=True
    )
    website_for_consumer = models.TextField(null=True, blank=True)
    telephone_number_for_consumers = models.TextField(null=True, blank=True)

    issued_by_top_25_institution = YesNoBooleanField(
        default=False, db_index=True
    )

    class Meta:
        indexes = [
            # Add an index to potentially optimize filtering on the
            # targeted_credit_tiers field. In practice PostgreSQL won't use
            # this index unless it's faster than doing a table scan, which it
            # likely won't be unless we have a very large number of cards.
            # Still,there's no harm in defining the index for future use.
            GinIndex(
                name="tccp_targeted_credit_tiers_idx",
                fields=["targeted_credit_tiers"],
                opclasses=["jsonb_path_ops"],
            ),
            # Do the same for the rewards field.
            GinIndex(
                name="tccp_rewards_idx",
                fields=["rewards"],
                opclasses=["jsonb_path_ops"],
            ),
            # Also add a joint index to speed up sorting by late fees.
            models.Index(
                fields=["late_fees", "late_fee_dollars"],
                name="tccp_late_fee_sorting_idx",
            ),
        ]

    objects = CardSurveyDataQuerySet.as_manager()

    @property
    def annual_fee_estimated(self):
        """Estimate a card's annual fee from its periodic fees.

        If a card has "Other" periodic fees, we can't accurately estimate its
        annual fee.
        """
        if "Other" in self.periodic_fee_type:
            return None

        fee = 0

        if "Annual" in self.periodic_fee_type and self.annual_fee:
            fee += self.annual_fee
        if "Monthly" in self.periodic_fee_type and self.monthly_fee:
            fee += 12 * self.monthly_fee
        if "Weekly" in self.periodic_fee_type and self.weekly_fee:
            fee += 52 * self.weekly_fee

        return fee

    @property
    def purchase_apr_data_incomplete(self):
        return self.purchase_apr_offered and not any(
            chain(
                *[
                    [
                        getattr(self, f"purchase_apr_{tier_column}_min"),
                        getattr(self, f"purchase_apr_{tier_column}_max"),
                    ]
                    for _, tier_column in enums.CreditTierColumns
                ]
            )
        )

    @property
    def issued_by_credit_union(self):
        return self.institution_type == "CU"

    @property
    def has_only_variable_late_fees(self):
        return [enums.LateFeeTypeChoices[2][0]] == self.late_fee_types

    @property
    def has_only_variable_over_limit_fees(self):
        return [
            enums.OverlimitFeeTypeChoices[1][0]
        ] == self.over_limit_fee_types
