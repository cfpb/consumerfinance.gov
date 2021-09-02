from functools import partial, wraps


def add_headers(view, headers):
    """Decorator that adds HTTP headers to a view's response.

    Usage:

      from app.views import myview
      wrapped_view = add_headers(myview, {'key': 'value', ...})

    """
    @wraps(view)
    def inner(request, *args, **kwargs):
        response = view(request, *args, **kwargs)

        for k, v in headers.items():
            response[k] = v

        return response

    return inner


akamai_no_store = partial(add_headers, headers={
    'Edge-Control': 'no-store',
    'Akamai-Cache-Control': 'no-store',
})
