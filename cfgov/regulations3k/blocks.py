from datetime import date

from django.db.models import Prefetch

from wagtail.core import blocks

from regulations3k.models.django import EffectiveVersion
from v1.atomic_elements import organisms


class RegulationsList(organisms.ModelBlock):
    model = "regulations3k.RegulationPage"
    ordering = "title"

    heading = blocks.CharBlock(required=False, help_text="Regulations list heading")
    more_regs_page = blocks.PageChooserBlock(help_text="Link to more regulations")
    more_regs_text = blocks.CharBlock(
        required=False, help_text="Text to show on link to more regulations"
    )

    def filter_queryset(self, qs, value):
        return qs.live()

    def get_queryset(self, value):
        qs = super().get_queryset(value)
        future_versions_qs = EffectiveVersion.objects.filter(
            draft=False, effective_date__gte=date.today()
        )
        qs = qs.prefetch_related(
            Prefetch(
                "regulation__versions",
                queryset=future_versions_qs,
                to_attr="future_versions",
            )
        )
        return qs

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["regulations"] = self.get_queryset(value)
        return context

    class Meta:
        icon = "list-ul"
        template = "regulations3k/regulations-listing.html"


class RegulationsListingFullWidthText(organisms.FullWidthText):
    regulations_list = RegulationsList()
