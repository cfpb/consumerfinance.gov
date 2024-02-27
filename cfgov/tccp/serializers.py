from rest_framework import serializers

from .models import CardSurveyData


class CardSurveyDataSerializer(serializers.HyperlinkedModelSerializer):
    periodic_fee_type = serializers.JSONField()
    purchase_apr = serializers.FloatField()
    rewards = serializers.JSONField()
    transfer_apr = serializers.FloatField()

    class Meta:
        model = CardSurveyData
        fields = [
            "balance_transfer_fees",
            "introductory_apr_offered",
            "periodic_fee_type",
            "product_name",
            "purchase_apr",
            "secured_card",
            "state_limitations",
            "rewards",
            "transfer_apr",
            "url",
        ]
        extra_kwargs = {
            "url": {"view_name": "tccp:card_detail"},
        }
