from collections import OrderedDict
from itertools import chain
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.stream_block import StreamValue


class JSHandler:
    def __init__(self, page):
        self.page = page
        self.js_dict = OrderedDict()
        self.generate_js_dict()

    def generate_js_dict(self):
        for key in ['template', 'organisms', 'molecules', 'atoms']:
            self.js_dict.update({key: []})
        self.page.add_page_js(self.js_dict)
        self.add_streamfield_js()
        for key, js_files in self.js_dict.iteritems():
            self.js_dict[key] = OrderedDict.fromkeys(js_files).keys()

    def get_js_dict(self):
        return self.js_dict

    # Gets the JS from the Streamfield data
    def add_streamfield_js(self):
        # Create a dictionary with keys ordered organisms, molecules, then atoms
        for child in self.get_streamfield_blocks():
            self.add_block_js(child.block)

    # Retrieves the stream values on a page from it's Streamfield
    def get_streamfield_blocks(self):
        lst = [value for key, value in vars(self.page).iteritems()
               if type(value) is StreamValue]
        return list(chain(*lst))

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
        try:
            if hasattr(obj.Media, 'js'):
                for key in self.js_dict.keys():
                    if obj.__module__.endswith(key):
                        self.js_dict[key] += obj.Media.js
                if not [key for key in self.js_dict.keys()
                        if obj.__module__.endswith(key)]:
                    self.js_dict.update({'other': obj.Media.js})
        except:
            pass
