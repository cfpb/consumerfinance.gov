import ast
from functools import wraps

from django import template
from django.http import Http404


register = template.Library()


def is_feature_view_active(feature_name):
    def _my_decorator(view_func):
        def _decorator(request, *args, **kwargs):

            active = is_feature_active(feature_name, request)

            if active:
                response = view_func(request, *args, **kwargs)
            else:
                raise Http404

            response = view_func(request, *args, **kwargs)

            return response
        return wraps(view_func)(_decorator)
    return _my_decorator


# if the feature is found in the environment scope, evaluate the value
# if true, enable feature. If false or it does not exist, disable it
def is_feature_active(feature_name, request):

    if feature_name in request.environ:
        return ast.literal_eval(request.environ[feature_name])

    return False


register.assignment_tag(is_feature_active)
