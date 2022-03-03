from wagtail.images.formats import Format, register_image_format

register_image_format(
    Format(
        "bleed",
        "Bleed into left/right margins",
        "richtext-image image-bleed",
        "width-1170",
    )
)
