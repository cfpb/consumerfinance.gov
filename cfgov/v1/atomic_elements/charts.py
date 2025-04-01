from wagtail import blocks

from wagtailcharts.blocks import ChartBlock as WagtailChartBlock

from v1 import blocks as v1_blocks


CHART_TYPES = (
    ("line", "Line Chart"),
    ("bar", "Vertical Bar Chart"),
    ("bar_horizontal", "Horizontal Bar Chart"),
)


CHART_COLORS = (
    ("#20aa3f", "CFPB Green"),
    ("#254b87", "Navy"),
    ("#7eb7e8", "Pacific 60"),
    ("#ffb858", "Gold 80"),
    ("#c55998", "Purple 80"),
    ("#addc91", "Green 60"),
    ("#1fa040", "Mid Dark Green"),
    ("#257675", "Teal"),
    ("#89b6b5", "Teal 60"),
    ("#d14124", "Red"),
    ("#e79e8e", "Red 60"),
    ("#0072ce", "Pacific"),
    ("#254b87", "Navy"),
    ("#dc731c", "Dark Gold"),
    ("#745745", "Dark Neutral"),
    ("#baa496", "Neutral 60"),
    ("#dc9cbf", "Purple 50"),
    ("#a01b68", "Dark Purple"),
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
    intro = blocks.RichTextBlock(required=False, icon="edit")
    description = blocks.TextBlock(
        required=False, help_text="Accessible description of the chart content"
    )
    data_source = blocks.TextBlock(
        required=False,
        help_text="Description of the data source",
    )
    date_published = blocks.CharBlock(
        required=False, help_text="When the underlying data was published"
    )
    download_text = blocks.CharBlock(
        required=False,
        help_text="Custom text for the chart download field. Required to "
        "display a download link.",
    )
    download_file = blocks.CharBlock(
        required=False,
        help_text="Location of a file to download",
    )
    notes = blocks.TextBlock(required=False, help_text="Note about the chart")

    def __init__(self, **kwargs):
        # Always override chart_types and colors with ours.
        super().__init__(
            chart_types=CHART_TYPES, colors=CHART_COLORS, **kwargs
        )

        # Create a more user-friendly ordering of this block's child blocks.
        #
        # This puts our content-focused blocks in front of the
        # chart-configuration blocks we inherit from wagtailcharts.
        #
        # child_blocks is an OrderedDict that comes from Wagtail's
        # StructBlock. This just calls OrderedDict.move_to_end() in the
        # order we want the blocks to appear.
        self.child_blocks.move_to_end("chart_type")
        self.child_blocks.move_to_end("datasets")
        self.child_blocks.move_to_end("settings")

        # We also want the eyebrow to appear above the title field.
        self.child_blocks.move_to_end("eyebrow", last=False)

    class Meta:
        label = "Chart"
        icon = "image"
        template = "v1/includes/organisms/wagtail-chart.html"

    # Load wagtailcharts scripts when block is included on a page instead of
    # by rendering a {% render_charts %} template tag.
    # https://github.com/overcastsoftware/wagtailcharts/blob/v0.5/wagtailcharts/templates/wagtailcharts/tags/render_charts.html
    class Media:
        js = [
            "wagtailcharts/js/chart-types.js?staticroot",
            "wagtailcharts/js/chart.js?staticroot",
            "wagtailcharts/js/stacked-100.js?staticroot",
            "wagtailcharts/js/chartjs-plugin-datalabels.min.js?staticroot",
            "wagtail-charts-chart-block.js",
            "wagtailcharts/js/wagtailcharts.js?staticroot",
        ]
        css = ["wagtail-chart.css"]
