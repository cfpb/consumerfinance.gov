import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from draftail_icons.rich_text import (
    IconEntityElementHandler,
    icon_entity_decorator,
)


@hooks.register("register_rich_text_features")
def register_icon_feature(features):
    """Register a Draftail feature for our SVG icons"""
    feature_name = "icon"

    # The editor plugin registers our JavaScript/CSS plugin that prompts a
    # user for an icon name and creates an ICON Entity for it in Draftail.
    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {
                "type": "ICON",
                "label": "Icon",
                "description": "SVG Icon",
            },
            js=["draftail_icons/js/draftail_icons.js"],
            css={"all": ["draftail_icons/css/draftail_icons.css"]},
        ),
    )

    # Converter rules convert our icon from the Draftail ContentState ICON
    # Entity to the form we store in the database and render.
    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                "span[data-icon-name]": IconEntityElementHandler("ICON")
            },
            "to_database_format": {
                "entity_decorators": {"ICON": icon_entity_decorator}
            },
        },
    )
