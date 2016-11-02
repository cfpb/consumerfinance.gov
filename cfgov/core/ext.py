from jinja2 import nodes
from jinja2.ext import Extension

from .utils import add_js_hash_to_request


class CSPScriptHashExtension(Extension):
    tags = {'hashedscript'}

    def parse(self, parser):

        # first token is the tag ('hashedscript'), skip it
        next(parser.stream)

        body = parser.parse_statements(['name:end_hashedscript'],
                                       drop_needle=True)

        context = nodes.ContextReference()

        return nodes.CallBlock(
            self.call_method('_hash_script', [context]),
            [],
            [],
            body
        )

    def _hash_script(self, context, caller):
        js = caller()

        request = context['request']

        add_js_hash_to_request(request, js)

        return u"<script>{js}</script>".format(js=js)


# nicer import name
csp = CSPScriptHashExtension
