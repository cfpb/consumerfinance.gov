from django.template.response import TemplateResponse

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from v1 import blocks as v1_blocks
from v1.atomic_elements import charts, organisms, schema
from v1.feeds import get_appropriate_rss_feed_url_for_page
from v1.models.learn_page import AbstractFilterPage


class BlogContent(blocks.StreamBlock):
    full_width_text = organisms.FullWidthText()
    info_unit_group = organisms.InfoUnitGroup()
    expandable = organisms.Expandable()
    expandable_group = organisms.ExpandableGroup()
    well = organisms.Well()
    video_player = organisms.VideoPlayer()
    email_signup = v1_blocks.EmailSignUpChooserBlock()
    simple_chart = organisms.SimpleChart()
    faq_schema = schema.FAQ(label="FAQ schema")
    how_to_schema = schema.HowTo(label="HowTo schema", max_num=1)
    wagtailchart_block = charts.ChartBlock()


class BlogPage(AbstractFilterPage):
    content = StreamField(
        BlogContent,
    )

    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=FieldPanel("content")
    )
    template = "v1/blog/blog_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["rss_feed"] = get_appropriate_rss_feed_url_for_page(
            self, request=request
        )

        return context

    @property
    def preview_modes(self):
        return super().preview_modes + [
            ("list_view", "List view"),
        ]

    def serve_preview(self, request, mode_name):
        if mode_name != "list_view":
            return super().serve_preview(request, mode_name)

        from v1.serializers import FilterPageSerializer

        serializer = FilterPageSerializer(self, context={"request": request})

        return TemplateResponse(
            request,
            "v1/blog/blog_page_list_preview.html",
            {
                "post": serializer.data,
            },
        )


class LegacyBlogContent(BlogContent):
    content = blocks.RawHTMLBlock(
        help_text="Content from WordPress unescaped."
    )
    reusable_text = v1_blocks.ReusableTextChooserBlock("v1.ReusableText")


class LegacyBlogPage(AbstractFilterPage):
    content = StreamField(
        LegacyBlogContent,
    )

    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=FieldPanel("content")
    )
    template = "v1/blog/legacy_blog_page.html"
