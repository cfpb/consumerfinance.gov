# Based off of http://jinja.pocoo.org/docs/2.10/extensions/
from django.core.cache import caches

from jinja2 import nodes
from jinja2.ext import Extension


class FragmentCacheExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(["cache"])

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        lineno = next(parser.stream).lineno

        # The first argument is the cache key
        args = [parser.parse_expression()]

        # The second argument is the cache's name
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression())

        # If there is a third argument, the user provided a timeout.
        # If not use None
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(["name:endcache"], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(
            self.call_method("_cache_support", args), [], [], body
        ).set_lineno(lineno)

    def _cache_support(self, key, cache_name, timeout, caller):
        """Helper callback."""
        fragment_cache = caches[cache_name]
        # try to load the block from the cache
        # if there is no fragment in the cache, render it and store
        # it in the cache.
        rv = fragment_cache.get(key)
        if rv is not None:
            return rv
        rv = caller()
        fragment_cache.add(key, rv, timeout)
        return rv
