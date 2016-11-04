from django import template

from ..utils import add_js_hash_to_request

register = template.Library()


def do_hashedscript(parser, token):
    nodelist = parser.parse(('end_hashedscript',))
    parser.delete_first_token()
    return HashedScriptNode(nodelist)


class HashedScriptNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        js = self.nodelist.render(context)

        request = context['request']

        add_js_hash_to_request(request, js)
        return u"<script>{js}</script>".format(js=js)

register.tag('hashedscript', do_hashedscript)
