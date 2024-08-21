from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)

from draftjs_exporter.dom import DOM

from core.templatetags.svg_icon import svg_icon


def icon_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.

    This function converts ICON entities into a <span> tag containing the SVG
    contents of the icon matching props["icon_name"]. The icon name itself is
    attached to the <span> in a data-icon-name attribute. This is what gets
    rendered on the frontend.
    """
    icon_name = props["icon-name"]
    icon = svg_icon(icon_name)
    icon_element = DOM.parse_html(icon)
    return DOM.create_element(
        "span", {"data-icon-name": icon_name}, icon_element
    )


class IconEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.

    This class converts a span[data-icon-name] tag to a Draft.js ICON entity.
    That entity is then rendered by the decorated we register in our Draftail
    plugin.
    """

    mutability = "SEGMENTED"

    def handle_endtag(self, name, state, contentstate):
        # Give the entity a space to attach to, since it has to have a range
        # of some length > 0, then pad it by one space.
        state.current_block.text += " "
        entity_range = state.current_entity_ranges.pop()
        entity_range.length = (
            len(state.current_block.text) - entity_range.offset
        )
        state.current_block.text += " "

    def get_attribute_data(self, attrs):
        return {
            "icon-name": attrs["data-icon-name"],
        }
