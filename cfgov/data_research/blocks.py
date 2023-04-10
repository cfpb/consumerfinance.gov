from wagtail import blocks


class MortgageDataDownloads(blocks.StructBlock):
    show_archives = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text=(
            "Check this box to allow the archival section to display. "
            "No section will appear if there are no archival downloads."
        ),
    )

    class Meta:
        label = "Mortgage Downloads Block"
        icon = "table"
        template = "data_research/mortgage-performance-downloads.html"
