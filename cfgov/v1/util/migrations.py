import logging
import re

from django.utils.deconstruct import deconstructible

from wagtail.blocks.migrations.operations import BaseBlockOperation


logger = logging.getLogger(__name__)


@deconstructible
class RegexAlterBlockValueOperation(BaseBlockOperation):
    """Alter a block's value with a regex pattern and replacement"""

    def __init__(self, pattern, replacement):
        super().__init__()
        self.pattern = re.compile(pattern)
        self.replacement = replacement

    def apply(self, block_value):
        if self.pattern.search(block_value):
            return self.pattern.sub(self.replacement, block_value)
        return block_value

    @property
    def operation_name_fragment(self):  # pragma: no cover
        return "regex_alter_block_value"


@deconstructible
class MoveContactPhoneFaxToPhonesOperation(BaseBlockOperation):
    """Move a Contact phone block's fax flag onto each of its phone numbers.

    Previously a single "fax" boolean on the phone block applied to every
    number in the block. Now each number has its own "is_fax" boolean.
    """

    def apply(self, block_value):
        is_fax = bool(block_value.pop("fax", False))

        for phone in block_value.get("phones", []):
            # Wagtail >= 2.16 stores list items as {"type": "item", "value"}.
            item = phone.get("value", phone)
            item["is_fax"] = is_fax

        return block_value

    @property
    def operation_name_fragment(self):  # pragma: no cover
        return "move_contact_phone_fax_to_phones"
