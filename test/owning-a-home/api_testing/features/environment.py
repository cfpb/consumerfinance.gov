import os
import ConfigParser
import logging


from pages.query_helper import QueryHelper
from pages.utils import Utils


def before_all(context):
    setup_config(context)
    setup_logger(context)

    context.query = QueryHelper(
        context.logger, context.base_url, context.mortgage_url)
    context.utils = Utils(context.query)

    context.logger.info('TEST ENVIRONMENT = %s, %s' %
                        (context.base_url, context.mortgage_url))


def before_feature(context, feature):
    context.logger.info('STARTING FEATURE %s' % feature)
    if context.browser == "Sauce":
        context.logger.info("Link to job: https://saucelabs.com/jobs/%s" %
                            context.base.driver.session_id)
        context.logger.info("SauceOnDemandSessionID=%s job-name=%s" %
                            (context.base.driver.session_id, feature.name))


def before_scenario(context, scenario):
    context.logger.info('starting scenario %s with row %s' %
                        (scenario, scenario._row))
    context.logger.info('starting feature %s, scenario %s, with row %s' %
                        (scenario.feature.name, scenario.name, scenario._row))


def after_scenario(context, scenario):
    context.logger.info('Finished scenario %s with row %s' %
                        (scenario, scenario._row))


def after_feature(context, feature):
    context.logger.info("after_feature")
    context.logger.info("Total time spent sleeping is %s" %
                        context.utils.time_spent_sleeping)


def after_all(context):
    pass


def setup_logger(context):
    # create logger
    logger = logging.getLogger('OAH_browser_tests: ')
    logger.setLevel(context.log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '[%(name)s] %(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    context.logger = logger


def setup_config(context):
    config = ConfigParser.ConfigParser()
    config.readfp(open('features/environment.cfg'))

    if config.has_option('logging', 'log_level'):
        context.log_level = config.get('logging', 'log_level')

    if config.has_option('general', 'testing_output'):
        context.directory = config.get('general', 'testing_output')
    else:
        context.directory = 'test-results'

    if not os.path.exists(context.directory):
        os.makedirs(context.directory)

    if config.has_option('browser_testing', 'delay'):
        context.delay_secs = config.getint('browser_testing', 'delay')
    else:
        context.delay_secs = 5

    if config.has_option('browser_testing', 'ratechecker_url'):
        context.base_url = config.get('browser_testing', 'ratechecker_url')
    else:
        context.base_url = 'http://localhost'

    if config.has_option('browser_testing', 'mortgageinsurance_url'):
        context.mortgage_url = config.get(
            'browser_testing', 'mortgageinsurance_url')
    else:
        context.mortgage_url = 'http://localhost'

    if config.has_option('browser_testing', 'browser'):
        context.browser = config.get('browser_testing', 'browser')
    else:
        context.browser = 'Chrome'

    if config.has_option('chrome_driver', 'chromedriver_path'):
        context.chromedriver_path = config.get('chrome_driver',
                                               'chromedriver_path')
    else:
        context.chromedriver_path = ''

    if config.has_option('browser_testing', 'take_screenshots'):
        context.take_screenshots = config.getboolean('browser_testing',
                                                     'take_screenshots')
    else:
        context.take_screenshots = False
