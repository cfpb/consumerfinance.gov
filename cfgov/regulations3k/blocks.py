from datetime import date

from django.db.models import Prefetch

from wagtail.wagtailcore import blocks

from regulations3k.models.django import EffectiveVersion
from v1.atomic_elements import organisms


class RegulationsList(organisms.ModelBlock):
    model = 'regulations3k.RegulationPage'
    ordering = 'title'

    heading = blocks.CharBlock(
        required=False,
        help_text='Regulations list heading'
    )
    more_regs_page = blocks.PageChooserBlock(
        help_text='Link to more regulations'
    )
    more_regs_text = blocks.CharBlock(
        required=False,
        help_text='Text to show on link to more regulations'
    )

    def filter_queryset(self, qs, value):
        return qs.live()

    def get_queryset(self, value):
        qs = super(RegulationsList, self).get_queryset(value)
        future_versions_qs = EffectiveVersion.objects.filter(
            draft=False,
            effective_date__gte=date.today()
        )
        qs = qs.prefetch_related(
            Prefetch(
                'regulation__versions',
                queryset=future_versions_qs,
                to_attr='future_versions'
            )
        )
        return qs

    def get_context(self, value, parent_context=None):
        context = super(RegulationsList, self).get_context(
            value, parent_context=parent_context
        )
        context['regulations'] = self.get_queryset(value)
        return context

    class Meta:
        icon = 'list-ul'
        template = 'regulations3k/regulations-listing.html'


class NotificationBlock(blocks.StructBlock):
    message = blocks.CharBlock(
        required=True,
        help_text='Main message of the notification'
    )
    explanation = blocks.TextBlock(
        required=False,
        help_text='An explanation for the notification'
    )
    notification_type = blocks.ChoiceBlock(
        required=True,
        choices=[
            ('success', 'Success'),
            ('warning', 'Warning'),
            ('error', 'Error'),
        ],
        default='warning'
    )

    def get_context(self, value, parent_context=None):
        context = super(NotificationBlock, self).get_context(
            value, parent_context=parent_context
        )

        if value.get('notification_type') == 'success':
            context['notification_icon'] = 'approved-round'
        else:
            context['notification_icon'] = (
                value.get('notification_type') + '-round'
            )

        return context

    class Meta:
        icon = 'warning'
        template = 'regulations3k/notification.html'


class RegulationsListingFullWidthText(organisms.FullWidthText):
    notification = NotificationBlock()
    regulations_list = RegulationsList()


class RegulationsFullWidthText(organisms.FullWidthText):
    notification = NotificationBlock()
