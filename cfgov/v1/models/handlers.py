from collections import OrderedDict
from itertools import chain
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.stream_block import StreamValue

from ..atomic_elements import ATOMIC_JS


class Handler(object):
    def __init__(self, page, request):
        self.page = page
        self.request = request

    def process(self, context):
        raise NotImplementedError

    # Retrieves the stream values on a page from it's Streamfield
    def get_streamfield_blocks(self):
        lst = [value for key, value in vars(self.page).iteritems()
               if type(value) is StreamValue]
        return list(chain(*lst))


class JSHandler(Handler):
    """
        Gathers all the JS files specific to this page and its current
        Streamfield's blocks and puts them in the template context.
    """
    def __init__(self, page, request):
        super(JSHandler, self).__init__(page, request)
        self.js_dict = OrderedDict()

    def process(self, context):
        self.generate_js_dict()
        context['media'] = self.js_dict

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
        for child in self.get_streamfield_blocks():
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
        try:
            if hasattr(obj.Media, 'js'):
                class_name = type(obj).__name__
                for key in self.js_dict:
                    if key in ATOMIC_JS:
                        if class_name in ATOMIC_JS[key]:
                            self.add_files(key, obj.Media.js)
                            break
                    elif key == 'other':
                        self.add_files(key, obj.Media.js)
                        break
        except AttributeError:
            pass

    def add_files(self, key, filenames):
        self.js_dict[key] += [name for name in filenames
                              if name not in self.js_dict[key]]
