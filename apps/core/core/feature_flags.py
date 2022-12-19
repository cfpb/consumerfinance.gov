from django.conf import settings

from flags import conditions


def _get_deploy_environment():
    return getattr(settings, "DEPLOY_ENVIRONMENT", None)


@conditions.register("environment is")
def environment_is(environment, **kwargs):
    return environment == _get_deploy_environment()


@conditions.register("environment is not")
def environment_is_not(environment, **kwargs):
    return environment != _get_deploy_environment()
