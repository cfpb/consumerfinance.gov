from collections import OrderedDict
from itertools import chain
from wagtail.wagtailcore import blocks

from . import Handler
from ...atomic_elements import ATOMIC_JS


class JSHandler(Handler):
    """
        Gathers all the JS files specific to this page and its current
        Streamfield's blocks and puts them in the template context.
    """
    def __init__(self, *args, **kwargs):
        super(JSHandler, self).__init__(*args, **kwargs)
        self.js_dict = OrderedDict()

    def process(self):
        self.generate_js_dict()
        if 'media' not in self.context:
            self.context['media'] = OrderedDict()
        self.context['media'].update(self.js_dict)

    def generate_js_dict(self):
        for key in ['template', 'organisms', 'molecules', 'atoms', 'other']:
            self.js_dict.update({key: []})
        self.page.add_page_js(self.js_dict)
        self.add_streamfield_js()
        for key, js_files in self.js_dict.iteritems():
            self.js_dict[key] = OrderedDict.fromkeys(js_files).keys()

    # Gets the JS from the Streamfield data
    def add_streamfield_js(self):
        # Create a dictionary with keys ordered organisms, molecules, then atoms
        blocks_dict = self.get_streamfield_blocks()
        for child in chain(*blocks_dict.values()):
            self.add_block_js(child.block)

    # Recursively search the blocks and classes for declared Media.js
    def add_block_js(self, block):
        self.assign_js(block)
        if issubclass(type(block), blocks.StructBlock):
            for child in block.child_blocks.values():
                self.add_block_js(child)
        elif issubclass(type(block), blocks.ListBlock):
            self.add_block_js(block.child_block)

    # Assign the Media js to the dictionary appropriately
    def assign_js(self, obj):
        if hasattr(obj, 'Media') and hasattr(obj.Media, 'js'):
            class_name = type(obj).__name__
            for key in self.js_dict:
                if key in ATOMIC_JS and class_name in ATOMIC_JS[key]:
                    self.add_files(key, obj.Media.js)
                    break
                elif key == 'other':
                    self.add_files(key, obj.Media.js)
                    break

    def add_files(self, key, filenames):
        self.js_dict[key] += [name for name in filenames
                              if name not in self.js_dict[key]]
