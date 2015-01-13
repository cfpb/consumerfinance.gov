from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from utils import Utils

import sys

# DEFAULT VALUES
default_driver_wait = 20


class Base(object):
    def __init__(self, logger, results_folder, base_url=r'http://localhost/',
                 driver=None, driver_wait=default_driver_wait, delay_secs=0):
        if driver is None:
            assert 'Driver is invalid or was not provided.'

        self.driver_wait = driver_wait
        self.base_url = base_url
        self.driver = driver
        self.chain = ActionChains(self.driver)
        self.logger = logger
        self.utils = Utils(delay_secs)
        self.results_folder = results_folder

    def go(self, relative_url=''):
        full_url = self.utils.build_url(self.base_url, relative_url)
        print full_url
        try:
            self.logger.info("Getting %s" % full_url)
            self.driver.get(full_url)
        except Exception:
            self.logger.info("Unexpected error running: %s" % full_url)
            self.logger.info("Exception type: %s" % sys.exc_info()[0])
            self.logger.info("Currently at: %s" % (self.driver.current_url))
            self.get_screenshot(full_url)
            raise

    def wait(self, driver_wait=default_driver_wait):
        return WebDriverWait(self.driver, driver_wait)

    def close_browser(self):
        self.utils.zzz(1)
        self.driver.quit()

    def sleep(self, time):
        self.utils.zzz(float(time))

    def get_screenshot(self, filename=None):
        if filename is None:
            filename = self.driver.current_url

        filename = "%s" % (filename.replace('/', '_'))
        full_path = '%s/%s.%s' % (self.results_folder, filename, 'png')
        self.logger.info("Saving screenshot to %s" % full_path)
        self.driver.save_screenshot(full_path)

    def get_page_title(self):
        return (self.driver.title)

    def get_current_url(self):
        return (self.driver.current_url)

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "window.scrollTo({0}, {1});".format(element.location['x'], 
                                                element.location['y']
                                               )
        )