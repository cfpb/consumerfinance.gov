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
