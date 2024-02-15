from rest_framework import serializers

from .models import CardSurveyData


class CardSurveyDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardSurveyData
        fields = ["url", "product_name"]
        extra_kwargs = {
            "url": {"view_name": "tccp:card_detail"},
        }
