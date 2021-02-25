from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.models.enforcement_action_page import (
    EnforcementActionDisposition, EnforcementActionPage
)


class EnforcementStatuteSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.get_statute_display()


class EnforcementDefendantTypeSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.get_defendant_type_display()


class EnforcementDocketSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.docket_number


class EnforcementStatusSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.get_status_display()


class EnforcementAtRiskSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.get_at_risk_group_display()


class EnforcementProductSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value.get_product_display()


class EnforcementDispositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnforcementActionDisposition
        fields = [
            'final_disposition',
            'final_disposition_type',
            'final_order_date',
            'dismissal_date',
            'final_order_consumer_redress',
            'final_order_consumer_redress_suspended',
            'final_order_other_consumer_relief',
            'final_order_other_consumer_relief_suspended',
            'final_order_disgorgement',
            'final_order_disgorgement_suspended',
            'final_order_civil_money_penalty',
            'final_order_civil_money_penalty_suspended',
            'estimated_consumers_entitled_to_relief',
        ]


class EnforcementActionSerializer(serializers.ModelSerializer):

    products = EnforcementProductSerializer(many=True)
    defendant_types = EnforcementDefendantTypeSerializer(many=True)
    docket_numbers = EnforcementDocketSerializer(many=True)
    statuses = EnforcementStatusSerializer(many=True)
    enforcement_dispositions = EnforcementDispositionSerializer(many=True)
    statutes = EnforcementStatuteSerializer(many=True)
    at_risk_groups = EnforcementAtRiskSerializer(many=True)

    class Meta:

        model = EnforcementActionPage
        fields = [
            'public_enforcement_action',
            'initial_filing_date',
            'defendant_types',
            'court',
            'docket_numbers',
            'settled_or_contested_at_filing',
            'products',
            'at_risk_groups',
            'enforcement_dispositions',
            'statuses',
            'statutes',
            'url',
        ]


# This API serves a JSON representation of the collection of official
# enforcement actions.
#
# EnforcementActionPage.all_actions() filters for live pages that are children
# of the Enforcement Actions filter page in the Wagtail tree.
#
# EnforcementActionSerializer creates a JSON representation of each
# EnforcementActionPage, including all of the metadata fields. See
# v1.tests.views.test_enforcement_api for more information.
#
# This endpoint is cached with Akamai. When any EnforcementActionPage is
# published, unpublished, or moved, the cache is invalidated by
# v1.signals.break_enforcement_cache. Listeners for those actions are
# registered in v1.apps.
class EnforcementAPIView(APIView):
    def get(self, request):
        queryset = EnforcementActionPage.all_actions()
        serializer = EnforcementActionSerializer(queryset, many=True)
        return Response(serializer.data)
