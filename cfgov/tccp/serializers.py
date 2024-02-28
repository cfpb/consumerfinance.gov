from rest_framework import serializers

from .models import CardSurveyData


class CardSurveyDataSerializer(serializers.HyperlinkedModelSerializer):
    periodic_fee_type = serializers.JSONField()
    purchase_apr_for_tier = serializers.FloatField()
    rewards = serializers.JSONField()
    transfer_apr_for_tier = serializers.FloatField()

    class Meta:
        model = CardSurveyData
        fields = [
            "balance_transfer_fees",
            "introductory_apr_offered",
            "periodic_fee_type",
            "product_name",
            "purchase_apr_for_tier",
            "secured_card",
            "state_limitations",
            "rewards",
            "transfer_apr_for_tier",
            "transfer_apr_min",
            "transfer_apr_max",
            "url",
        ]
        extra_kwargs = {
            "url": {"view_name": "tccp:card_detail"},
        }
