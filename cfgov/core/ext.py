from jinja2 import nodes
from jinja2.ext import Extension

from .utils import hash_for_script


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
        if not hasattr(request, 'script_hashes'):
            request.script_hashes = []

        hash = hash_for_script(js)
        request.script_hashes.append(hash)
        return u"<script>{js}</script>".format(js=js)


# nicer import name
csp = CSPScriptHashExtension
