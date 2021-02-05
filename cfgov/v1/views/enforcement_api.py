import csv

from django.http import HttpResponse

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


class EnforcementCSVSerializer():
    header_row = [
        "Public Enforcement Action",
        "Initial Filing Date",
        "Defendant / Respondent Type",
        "Forum",
        "Court",
        "Docket Number",
        "Settled or Contested at Filing",
        "Status",
        "Product(s)",
        "At Risk Group(s)",
        "Statute(s)/Regulation(s)",
        "Total Consumer Relief",
        "Total Civil Money Penalties",
        "Final Disposition",
        "Final Disposition Type",
        "Final Order Date",
        "Dismissal Date",
        "Final Order Total Consumer Relief",
        "Final Order Total Consumer Relief Suspended",
        "Final Order Total Consumer Relief Not Suspended",
        "Final Order Consumer Redress",
        "Final Order Consumer Redress Suspended",
        "Final Order Consumer Redress Not Suspended",
        "Final Order Other Consumer Relief",
        "Final Order Other Consumer Relief Suspended",
        "Final Order Other Consumer Relief Not Suspended",
        "Final Order Disgorgement",
        "Final Order Disgorgement Suspended",
        "Final Order Disgorgement Not Suspended",
        "Final Order Civil Money Penalty",
        "Final Order Civil Money Penalty Suspended",
        "Final Order Civil Money Penalty Not Suspended",
        "Estimated Consumers Entitled to Relief in Final",
    ]

    @classmethod
    def multiple(cls, items, getter):
        return ";".join([
            getattr(item, getter)() for item in items
        ])

    @classmethod
    def serialize_enforcement_action(cls, disp):
        defendant_types = cls.multiple(disp.action.defendant_types.all(),
                                       'get_defendant_type_display')

        docket_numbers = ";".join([
            docket.docket_number
            for docket in disp.action.docket_numbers.all()
        ])

        forums = cls.multiple(disp.action.categories.all(), 'get_name_display')

        statuses = cls.multiple(disp.action.statuses.all(),
                                'get_status_display')

        products = cls.multiple(disp.action.products.all(),
                                'get_product_display')

        at_risk_groups = cls.multiple(disp.action.at_risk_groups.all(),
                                      'get_at_risk_group_display')

        statutes = cls.multiple(disp.action.statutes.all(),
                                'get_statute_display')

        consumer_relief = sum([
            disp.final_order_consumer_redress,
            disp.final_order_other_consumer_relief,
        ])

        consumer_relief_suspended = sum([
            disp.final_order_consumer_redress_suspended,
            disp.final_order_other_consumer_relief_suspended,
        ])

        data = [
            disp.action.public_enforcement_action,
            disp.action.initial_filing_date,
            defendant_types,
            forums,
            disp.action.court,
            docket_numbers,
            disp.action.get_settled_or_contested_at_filing_display(),
            statuses,
            products,
            at_risk_groups,
            statutes,
            disp.action.total_consumer_relief(),
            disp.action.total_civil_penalties(),
            disp.final_disposition,
            disp.get_final_disposition_type_display(),
            disp.final_order_date,
            disp.dismissal_date,
            consumer_relief,
            consumer_relief_suspended,
            consumer_relief - consumer_relief_suspended,
            disp.final_order_consumer_redress,
            disp.final_order_consumer_redress_suspended,
            disp.final_order_consumer_redress - disp.final_order_consumer_redress_suspended,  # noqa E501
            disp.final_order_other_consumer_relief,
            disp.final_order_other_consumer_relief_suspended,
            disp.final_order_other_consumer_relief - disp.final_order_other_consumer_relief_suspended,  # noqa E501
            disp.final_order_disgorgement,
            disp.final_order_disgorgement_suspended,
            disp.final_order_disgorgement - disp.final_order_disgorgement_suspended,  # noqa E501
            disp.final_order_civil_money_penalty,
            disp.final_order_civil_money_penalty_suspended,
            disp.final_order_civil_money_penalty - disp.final_order_civil_money_penalty_suspended,  # noqa E501
            disp.estimated_consumers_entitled_to_relief,
        ]
        return data


# This API serves a CSV file representation of the collection of official
# enforcement actions. The CSV output has one row per final disposition, since
# some enforcement actions have multiple final dispositions.
#
# EnforcementCSVSerializer serializes each enforcement action-final
# disposition combination into a single CSV row. For fields that can have
# multiple entries, such as Docket Number and Statute, multiple responses are
# separated by semicolons.
#
# This endpoint is cached with Akamai. When any EnforcementActionPage is
# published, unpublished, or moved, the cache is invalidated by
# v1.signals.break_enforcement_cache. Listeners for those actions are
# registered in v1.apps.
class EnforcementCSVView():
    @classmethod
    def get(cls, request):
        queryset = EnforcementActionDisposition.all_dispositions()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="enforcement.csv"'
        writer = csv.writer(response)
        writer.writerow(EnforcementCSVSerializer.header_row)
        for disposition in queryset:
            row = EnforcementCSVSerializer.serialize_enforcement_action(disposition)  # noqa E501
            writer.writerow(row)

        return response
