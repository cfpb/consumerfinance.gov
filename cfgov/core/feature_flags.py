from itertools import chain

from django.conf import settings

from flags import conditions

from core.split_testing_clusters import CLUSTERS


def _get_deploy_environment():
    return getattr(settings, 'DEPLOY_ENVIRONMENT', None)


@conditions.register('environment is')
def environment_is(environment, **kwargs):
    return environment == _get_deploy_environment()


@conditions.register('environment is not')
def environment_is_not(environment, **kwargs):
    return environment != _get_deploy_environment()


@conditions.register('in split testing cluster')
def in_split_testing_cluster(cluster_group, page, **kwargs):
    clusters = CLUSTERS[cluster_group]
    lookup_value = getattr(page, 'split_test_id', page.id)
    return lookup_value in chain(*clusters.values())
