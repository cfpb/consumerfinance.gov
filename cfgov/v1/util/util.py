from time import time

from django.core.exceptions import ValidationError


ERROR_MESSAGES = {
    "CHECKBOX_ERRORS": {
        "required": 'Please select at least one of the "%s" options.'
    },
    "DATE_ERRORS": {
        "invalid": "You have entered an invalid date.",
    },
}


def get_unique_id(prefix="", suffix=""):
    index = hex(int(time() * 10000000))[2:]
    return prefix + str(index) + suffix


def extended_strftime(dt, format):
    """
    Extend strftime with additional patterns:
    _m for custom month abbreviations,
    _d for day values without leading zeros.
    """
    _MONTH_ABBREVIATIONS = [
        None,
        "Jan.",
        "Feb.",
        "Mar.",
        "Apr.",
        "May",
        "Jun.",
        "Jul.",
        "Aug.",
        "Sept.",
        "Oct.",
        "Nov.",
        "Dec.",
    ]

    format = format.replace("%_d", dt.strftime("%d").lstrip("0"))
    format = format.replace("%_m", _MONTH_ABBREVIATIONS[dt.month])
    return dt.strftime(format)


def validate_social_sharing_image(image):
    """Raises a validation error if the image is too large or too small."""
    if image and (image.width > 4096 or image.height > 4096):
        raise ValidationError(
            "Social sharing image must be less than 4096w x 4096h"
        )
