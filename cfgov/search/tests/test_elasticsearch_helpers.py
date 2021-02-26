from django.test import TestCase, override_settings

from search.elasticsearch_helpers import environment_specific_index


class TestEnvironmentSpecificIndex(TestCase):

    @override_settings(DEPLOY_ENVIRONMENT='local')
    def test_environment_specific_index_excludes_deploy_env_local(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'index')

    @override_settings(DEPLOY_ENVIRONMENT='production')
    def test_environment_specific_index_excludes_deploy_env_production(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'index')

    @override_settings(DEPLOY_ENVIRONMENT=None)
    def test_environment_specific_index_excludes_deploy_env_undefined(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'index')

    @override_settings(DEPLOY_ENVIRONMENT='test')
    def test_environment_specific_index_includes_deploy_env(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'test-index')

    # Handle uppercase deploy environment vars (for Jenkins)
    @override_settings(DEPLOY_ENVIRONMENT='PRODUCTION')
    def test_environment_specific_index_excludes_deploy_env_PRODUCTION(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'index')

    @override_settings(DEPLOY_ENVIRONMENT='TEST')
    def test_environment_specific_index_lowercases_index(self):
        name = environment_specific_index('index')
        self.assertEqual(name, 'test-index')
