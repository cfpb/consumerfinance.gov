from functools import wraps


def add_headers(view, headers):
    """Wrapper that adds HTTP headers to a view's response.

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
