import re

from django.conf import settings

from flags import conditions


def _get_deploy_environment():
    return getattr(settings, 'DEPLOY_ENVIRONMENT', None)


@conditions.register('environment is')
def environment_is(environment, **kwargs):
    return environment == _get_deploy_environment()


@conditions.register('environment is not')
def environment_is_not(environment, **kwargs):
    return environment != _get_deploy_environment()


@conditions.register('in split testing cluster')
def split_test_is_active(clusters, request, **kwargs):
    match = re.match(request.path, r'^/ask-cfpb/.+-(\d+)/$')
    if match:
        for cluster in clusters:
            if match.groups(1) in cluster['answer_ids']:
                return True
    else:
        for cluster in clusters:
            if request.path in cluster['page_path']:
                return True

    return False
