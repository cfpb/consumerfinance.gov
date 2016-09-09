from collections import OrderedDict
from itertools import chain
from wagtail.wagtailcore import blocks

from ..handlers import Handler
from v1.util import util


class JSEnum:
    atoms     = []
    blocks    = []
    molecules = []
    organisms = [
        'BaseExpandable',
        'Expandable',
        'ExpandableGroup',
        'FilterControls',
    ]


class JSHandler(Handler):
    """
        Gathers all the JS files specific to this page and its current
        Streamfields' blocks and sets them in the template context.
    """
    def __init__(self, page, request, context):
        super(JSHandler, self).__init__(page, request, context)
        atomic_types = ['template', 'organisms', 'molecules', 'atoms']
        self.js_dict = OrderedDict([(at, []) for at in atomic_types])

    def process(self):
        """
        Sets media in context to the configured js_dict.
        """
        self.set_js_dict()

        if 'media' not in self.context:
            self.context['media'] = self.js_dict

        elif isinstance(self.context['media'], OrderedDict):
            self.context['media'].update(self.js_dict)

    def set_js_dict(self):
        """
        Sets the js_dict's keys to valid files.
        """
        self.js_dict['template'] = self.page.get_page_js()

        blocks_dict = util.get_streamfields(self.page)
        for child in chain(*blocks_dict.values()):
            self.set_block_js(child.block)

    def set_block_js(self, block):
        """
        Recursively search the blocks and classes for declared Media.js.
        """
        self.assign_js(block)

        if issubclass(type(block), blocks.StructBlock):
            for child in block.child_blocks.values():
                self.set_block_js(child)

        elif issubclass(type(block), blocks.ListBlock):
            self.set_block_js(block.child_block)

    def assign_js(self, obj):
        """
        Assign the obj.Media.js to the dictionary.
        """
        key = self.is_valid(obj)
        if key:
            self.js_dict[key] += [
                name for name in obj.Media.js if name not in self.js_dict[key]
            ]

    def is_valid(self, obj):
        """
        Checks against the enum for the validity of the object's JS and returns
        the key if it is.
        """
        if hasattr(obj, 'Media') and hasattr(obj.Media, 'js'):
            class_name = obj.__class__.__name__

            for key in self.js_dict:
                approved_files = getattr(JSEnum, key, None)
                if approved_files and class_name in approved_files:
                    return key
        return False
