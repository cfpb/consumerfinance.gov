import os
import ConfigParser
import logging
import httplib
import base64
import multiprocessing

from datetime import datetime
from selenium import webdriver
from elasticsearch import Elasticsearch
from sheer.wsgi import app_with_config

from pages.screenshot import Screenshot
from pages.base import Base
from pages.navigation import Navigation
from pages.newsroom import Newsroom
from pages.utils import Utils


try:
    import json
except ImportError:
    import simplejson as json


index_name = "cfgov_test"
root = os.path.join(os.getcwd(), '../..')

class LiveServer(object):
    def __init__(self):
        config = dict(debug=False,
                      location=root,
                      elasticsearch=[{'host': 'localhost', 'port': 9200}],
                      index=index_name)
        self.app = app_with_config(config)
        worker = lambda app, port: app.run(host='0.0.0.0', port=7000, use_reloader=False)
        self.process = multiprocessing.Process(
                    target=worker, args=(self.app, 7000)
                  )
        self.process.start()

    def terminate(self):
        self.process.terminate()


def before_all(context):
    setup_config(context)
    setup_logger(context)

    if context.browser == 'Sauce':
        context.logger.info("Using Sauce Labs")
        desired_capabilities = {
            'name': os.getenv('SELENIUM_NAME',
                              'cfgov-refresh browser tests ') + str(datetime.now()),
            'platform': os.getenv('SELENIUM_PLATFORM', 'WINDOWS 7'),
            'browserName': os.getenv('SELENIUM_BROWSER', 'chrome'),
            'version': int(os.getenv('SELENIUM_VERSION', 33)),
            'max-duration': 7200,
            'record-video': os.getenv('SELENIUM_VIDEO', True),
            'video-upload-on-pass': os.getenv('SELENIUM_VIDEO_UPLOAD_ON_PASS',
                                              True),
            'record-screenshots': os.getenv('SELENIUM_SCREENSHOTS', False),
            'command-timeout': int(os.getenv('SELENIUM_CMD_TIMEOUT', 30)),
            'idle-timeout': int(os.getenv('SELENIUM_IDLE_TIMEOUT', 10)),
            'tunnel-identifier': os.getenv('SELENIUM_TUNNEL'),
        }

        context.logger.info("Running Sauce with capabilities: %s" %
                            desired_capabilities)

        sauce_config = {"username": os.getenv('SAUCE_USERNAME'),
                        "access-key": os.getenv("SAUCE_ACCESS_KEY")}
        context.sauce_config = sauce_config

        driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" %
            (sauce_config['username'], sauce_config['access-key'])
        )

    else:
        driver = webdriver.Chrome(context.chromedriver_path)

    context.base = Base(context.logger, context.directory,
                        context.base_url, driver, 10, context.delay_secs)
    context.newsroom = Newsroom(context.logger, context.directory,
                        context.base_url, driver, 10, context.delay_secs)
    context.navigation = Navigation(context.logger, context.directory,
                                    context.base_url,
                                    driver, 10, context.delay_secs)
    context.screenshot = Screenshot(context.base, context.take_screenshots)

    context.utils = Utils(context.base)

    context.server = LiveServer()

    context.logger.info('TEST ENVIRONMENT = %s' % context.base_url)

    es = Elasticsearch()
    if es.indices.exists(index_name):
        es.indices.delete(index_name)
    es.indices.create(index=index_name)

    # Create the mappings
    create_mapping('newsroom', os.path.join(root, '_settings/posts_mappings.json'))
    create_mapping('watchroom', os.path.join(root, '_settings/posts_mappings.json'))

    # Index the documents
    index_documents('newsroom', os.path.join(root, '_tests/browser_testing/fixtures/newsroom.json'))
    index_documents('views', os.path.join(root, '_tests/browser_testing/fixtures/views.json'))
    index_documents('watchroom', os.path.join(root, '_tests/browser_testing/fixtures/watchroom.json'))

    
    

def before_feature(context, feature):
    context.logger.info('STARTING FEATURE %s' % feature)
    if context.browser == "Sauce":
        context.logger.info("Link to job: https://saucelabs.com/jobs/%s" %
                            context.base.driver.session_id)
        context.logger.info("SauceOnDemandSessionID=%s job-name=%s" %
                            (context.base.driver.session_id, feature.name))


def before_scenario(context, scenario):
    # Ensure each scenario starts with a full browser window.
    context.base.driver.maximize_window()
    context.logger.info('starting scenario %s with row %s' %
                        (scenario, scenario._row))
    context.logger.info('starting feature %s, scenario %s, with row %s' %
                        (scenario.feature.name, scenario.name, scenario._row))


def after_scenario(context, scenario):
    context.logger.info('Finished scenario %s with row %s' %
                        (scenario, scenario._row))


def after_feature(context, feature):
    context.logger.info("Total time spent sleeping is %s" %
                        context.base.utils.time_spent_sleeping)


def after_all(context):
    context.base.close_browser()
    if context.browser == 'Sauce':
        base64string = base64.encodestring('%s:%s' %
                                           (context.sauce_config['username'],
                                            context.sauce_config['access-key']
                                            ))[:-1]

        body_content = json.dumps({"passed": not context.failed})
        context.logger.info("Updating sauce job with %s" % body_content)
        # If a proxy is present then use it, otherwise connect directly to saucelabs
        http_proxy = os.getenv('http_proxy', None)
        if http_proxy:
            if http_proxy.startswith("http://"):
                http_proxy = http_proxy[7:]
            connection = httplib.HTTPConnection(http_proxy)
        else:    
            connection = httplib.HTTPConnection("saucelabs.com")

        connection.request('PUT', 'http://saucelabs.com/rest/v1/%s/jobs/%s' %
                           (context.sauce_config['username'],
                            context.base.driver.session_id),
                           body_content,
                           headers={"Authorization": "Basic %s" % base64string})
        result = connection.getresponse()
        context.logger.info(result.read())
        context.logger.info("Sauce update status: %s" % result.status)

    es = Elasticsearch()
    es.indices.delete(index_name)
    context.server.terminate()


def setup_logger(context):
    # create logger
    logger = logging.getLogger('cfgov-refresh_browser_tests: ')
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
        context.log_level = int(config.get('logging', 'log_level'))

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

    if config.has_option('browser_testing', 'base_url'):
        context.base_url = config.get('browser_testing', 'base_url')
    else:
        context.base_url = 'http://localhost'

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

def create_mapping(doc_type, mapping_json_path):
    es = Elasticsearch()
    mapping_json = open(os.path.join(root, mapping_json_path))
    mapping = json.load(mapping_json)
    es.indices.put_mapping(index=index_name,
                           doc_type=doc_type,
                           body={doc_type: mapping})

def index_documents(doc_type, json_path):
    es = Elasticsearch()
    json_file = open(os.path.join(root, json_path))
    documents = json.load(json_file)

    for document in documents:
        es.create(index=index_name,
                  doc_type=doc_type,
                  id=document['_id'],
                  body=document)