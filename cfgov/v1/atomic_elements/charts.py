from wagtail import blocks

from wagtailcharts.blocks import ChartBlock as WagtailChartBlock

from v1 import blocks as v1_blocks

# Bring tables into this module to maintain import structure across the project
from v1.atomic_elements.tables import (  # noqa: F401
    CaseDocketTable,
    ConsumerReportingCompanyTable,
    ContactUsTable,
    Table,
)


CHART_TYPES = (
    ("line", "Line Chart"),
    ("bar", "Vertical Bar Chart"),
    ("bar_horizontal", "Horizontal Bar Chart"),
    ("pie", "Pie Chart"),
)


CHART_COLORS = (
    ("#addc91", "Green 60"),
    ("#1fa040", "Mid Dark Green"),
    ("#257675", "Teal"),
    ("#89b6b5", "Teal 60"),
    ("#d14124", "Red"),
    ("#e79e8e", "Red 60"),
    ("#0072ce", "Pacific"),
    ("#7eb7e8", "Pacific 60"),
    ("#254b87", "Navy"),
    ("#9daecc", "Navy 50"),
    ("#dc731c", "Dark Gold"),
    ("#ffc372", "Gold 70"),
    ("#745745", "Dark Neutral"),
    ("#baa496", "Neutral 60"),
    ("#a01b68", "Dark Purple"),
    ("#dc9cbf", "Purple 50"),
    ("#d2d3d5", "Gray 20"),
)


class ChartBlock(WagtailChartBlock):
    eyebrow = blocks.CharBlock(
        required=False,
        help_text=(
            "Optional: Adds an H5 eyebrow above H1 heading text. "
            "Only use in conjunction with heading."
        ),
        label="Pre-heading",
    )
    title = v1_blocks.HeadingBlock(required=False)
    intro = blocks.RichTextBlock(icon="edit")
    description = blocks.TextBlock(
        required=True, help_text="Accessible description of the chart content"
    )
    data_source = blocks.TextBlock(
        required=False,
        help_text="Description of the data source",
    )
    date_published = blocks.CharBlock(
        required=False, help_text="When the underlying data was published"
    )
    download_file = blocks.CharBlock(
        required=False,
        help_text="Location to download this chart's data",
        label="Download",
    )
    notes = blocks.TextBlock(required=False, help_text="Note about the chart")

    chart_type = blocks.ChoiceBlock(
        choices=CHART_TYPES,
        default="datetime",
        required=True,
    )

    def __init__(self, **kwargs):
        # Always override chart_types and colors with ours
        super().__init__(
            chart_types=CHART_TYPES, colors=CHART_COLORS, **kwargs
        )

    class Meta:
        label = "Chart"
        icon = "image"
        template = "v1/includes/organisms/wagtail-chart.html"

    # Load wagtailcharts scripts when block is included on a page instead of
    # by rendering a {% render_charts %} template tag.
    # https://github.com/overcastsoftware/wagtailcharts/blob/v0.5/wagtailcharts/templates/wagtailcharts/tags/render_charts.html
    class Media:
        js = [
            "wagtailcharts/js/accounting.js?staticroot",
            "wagtailcharts/js/chart-types.js?staticroot",
            "wagtailcharts/js/chart.js?staticroot",
            "wagtailcharts/js/stacked-100.js?staticroot",
            "wagtailcharts/js/chartjs-plugin-datalabels.min.js?staticroot",
            "wagtail-charts-chart-block.js",
            "wagtailcharts/js/wagtailcharts.js?staticroot",
        ]
