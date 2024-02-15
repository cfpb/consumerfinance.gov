import re

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Q

from . import enums
from .fields import CurrencyField, JSONListField, YesNoBooleanField


REPORT_DATE_REGEX = re.compile(r"Data as of (\w+ \d+)")


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


class CardSurveyData(models.Model):
    institution_name = models.TextField()
    product_name = models.TextField()
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
    purchase_apr_poor = models.FloatField(null=True, blank=True)
    purchase_apr_good = models.FloatField(null=True, blank=True)
    purchase_apr_great = models.FloatField(null=True, blank=True)
    purchase_apr_min = models.FloatField(null=True, blank=True)
    purchase_apr_median = models.FloatField(null=True, blank=True)
    purchase_apr_max = models.FloatField(null=True, blank=True)
    introductory_apr_offered = YesNoBooleanField()
    introductory_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    intro_apr_poor = models.FloatField(null=True, blank=True)
    intro_apr_good = models.FloatField(null=True, blank=True)
    intro_apr_great = models.FloatField(null=True, blank=True)
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
    transfer_apr_poor = models.FloatField(null=True, blank=True)
    transfer_apr_good = models.FloatField(null=True, blank=True)
    transfer_apr_great = models.FloatField(null=True, blank=True)
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
    advance_apr_poor = models.FloatField(null=True, blank=True)
    advance_apr_good = models.FloatField(null=True, blank=True)
    advance_apr_great = models.FloatField(null=True, blank=True)
    advance_apr_min = models.FloatField(null=True, blank=True)
    advance_apr_median = models.FloatField(null=True, blank=True)
    advance_apr_max = models.FloatField(null=True, blank=True)
    grace_period_offered = YesNoBooleanField()
    grace_period = models.PositiveIntegerField(null=True, blank=True)
    minimum_finance_charge = YesNoBooleanField()
    minimum_finance_charge_dollars = CurrencyField(null=True, blank=True)
    balance_computation_method = JSONListField(
        choices=enums.BalanceComputationChoices
    )
    balance_computation_method_details = models.TextField(
        null=True, blank=True
    )
    periodic_fee_type = JSONListField(
        choices=enums.PeriodicFeeTypeChoices, blank=True
    )
    annual_fee = CurrencyField(null=True, blank=True)
    monthly_fee = CurrencyField(null=True, blank=True)
    weekly_fee = CurrencyField(null=True, blank=True)
    other_periodic_fee_name = models.TextField(null=True, blank=True)
    other_periodic_fee_amount = CurrencyField(null=True, blank=True)
    other_periodic_fee_frequency = models.TextField(null=True, blank=True)
    fee_varies = YesNoBooleanField(null=True, blank=True)
    periodic_min = CurrencyField(null=True, blank=True)
    periodic_max = CurrencyField(null=True, blank=True)
    fee_explanation = models.TextField(null=True, blank=True)
    purchase_transaction_fees = YesNoBooleanField()
    purchase_transaction_fee_type = JSONListField(
        choices=enums.PurchaseTransactionFeeTypeChoices, blank=True
    )
    purchase_transaction_fee_dollars = CurrencyField(null=True, blank=True)
    purchase_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_purchase_transaction_fee_amount = CurrencyField(
        null=True, blank=True
    )
    purchase_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    balance_transfer_fees = YesNoBooleanField()
    balance_transfer_fee_types = JSONListField(
        choices=enums.BalanceTransferFeeTypeChoices, blank=True
    )
    balance_transfer_fee_dollars = CurrencyField(null=True, blank=True)
    balance_transfer_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_balance_transfer_fee_amount = CurrencyField(null=True, blank=True)
    balance_transfer_fee_calculation = models.TextField(null=True, blank=True)
    cash_advance_fees = YesNoBooleanField()
    cash_advance_fee_for_each_transaction = YesNoBooleanField(
        null=True, blank=True
    )
    cash_advance_fee_types = JSONListField(
        choices=enums.CashAdvanceFeeTypeChoices, blank=True
    )
    cash_advance_fee_dollars = CurrencyField(null=True, blank=True)
    cash_advance_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_cash_advance_fee_amount = CurrencyField(null=True, blank=True)
    cash_advance_fee_calculation = models.TextField(null=True, blank=True)
    foreign_transaction_fees = YesNoBooleanField()
    foreign_transaction_fees_types = JSONListField(
        choices=enums.ForeignTransactionFeeTypeChoices, blank=True
    )
    foreign_transaction_fee_dollars = CurrencyField(null=True, blank=True)
    foreign_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_foreign_transaction_fee_amount = CurrencyField(
        null=True, blank=True
    )
    foreign_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    late_fees = YesNoBooleanField()
    late_fee_types = JSONListField(
        choices=enums.LateFeeTypeChoices, blank=True
    )
    late_fee_dollars = CurrencyField(null=True, blank=True)
    late_fee_six_month_billing_cycle = CurrencyField(null=True, blank=True)
    late_fee_policy_details = models.TextField(null=True, blank=True)
    fee_varies36 = YesNoBooleanField(null=True, blank=True)
    minimum37 = CurrencyField(null=True, blank=True)
    maximum38 = CurrencyField(null=True, blank=True)
    fee_explanation39 = models.TextField(null=True, blank=True)
    over_limit_fees = YesNoBooleanField()
    over_limit_fee_types = JSONListField(
        choices=enums.OverlimitFeeTypeChoices, blank=True
    )
    over_limit_fee_dollars = CurrencyField(null=True, blank=True)
    overlimit_fee_detail = models.TextField(null=True, blank=True)
    other_fees = YesNoBooleanField()
    additional_fees = YesNoBooleanField(null=True, blank=True)
    other_fee_name = models.TextField(null=True, blank=True)
    other_fee_amount = CurrencyField(null=True, blank=True)
    other_fee_explanation = models.TextField(null=True, blank=True)
    other_fee_name_2 = models.TextField(null=True, blank=True)
    other_fee_amount_2 = CurrencyField(null=True, blank=True)
    other_fee_explanation_2 = models.TextField(null=True, blank=True)
    other_fee_name_3 = models.TextField(null=True, blank=True)
    other_fee_amount_3 = CurrencyField(null=True, blank=True)
    other_fee_explanation_3 = models.TextField(null=True, blank=True)
    other_fee_name_4 = models.TextField(null=True, blank=True)
    other_fee_amount_4 = CurrencyField(null=True, blank=True)
    other_fee_explanation_4 = models.TextField(null=True, blank=True)
    other_fee_name_5 = models.TextField(null=True, blank=True)
    other_fee_amount_5 = CurrencyField(null=True, blank=True)
    other_fee_explanation_5 = models.TextField(null=True, blank=True)
    fee_varies56 = YesNoBooleanField(null=True, blank=True)
    minimum57 = CurrencyField(null=True, blank=True)
    maximum58 = CurrencyField(null=True, blank=True)
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

    class Meta:
        # Add an index to potentially optimize filtering on the
        # targeted_credit_tiers field. In practice PostgreSQL won't use this
        # index unless it's faster than doing a table scan, which it likely
        # won   't be unless we have a very large number of cards. Still, there's
        # no harm in defining the index in case or for future use.
        indexes = [
            GinIndex(
                name="targeted_credit_tiers_idx",
                fields=["targeted_credit_tiers"],
                opclasses=["jsonb_path_ops"],
            ),
        ]

    objects = CardSurveyDataQuerySet.as_manager()

    @property
    def state_limitations(self):
        """Get the list of states in which a given card is available.

        Returns None if the card is available everywhere.
        """
        if self.availability_of_credit_card_plan == "One State/Territory":
            return [self.state]
        elif self.availability_of_credit_card_plan == "Regional":
            return self.state_multiple
