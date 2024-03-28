from rest_framework import serializers

from .fields import JSONListField
from .models import CardSurveyData


class CardSurveyDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardSurveyData
        fields = "__all__"
        extra_kwargs = {
            "url": {"lookup_field": "slug", "view_name": "tccp:card_detail"},
        }

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(
            field_name, model_field
        )

        # Our JSONListField inherits from JSONField but also supports a
        # "choices" argument, which breaks some assumptions made by
        # django-rest-framework. This code is needed to ensure that
        # JSONListFields are serialized properly as JSON.
        if isinstance(model_field, JSONListField):
            field_kwargs.pop("encoder"),
            field_kwargs.pop("decoder")

        return field_class, field_kwargs


class CardSurveyDataListSerializer(CardSurveyDataSerializer):
    purchase_apr_for_tier = serializers.FloatField()
    purchase_apr_for_tier_rating = serializers.IntegerField()
    transfer_apr_for_tier = serializers.FloatField()

    class Meta(CardSurveyDataSerializer.Meta):
        fields = [
            "institution_name",
            "periodic_fee_type",
            "product_name",
            "purchase_apr_for_tier",
            "purchase_apr_for_tier_rating",
            "rewards",
            "top_25_institution",
            "transfer_apr_for_tier",
            "transfer_apr_min",
            "transfer_apr_max",
            "url",
        ]
