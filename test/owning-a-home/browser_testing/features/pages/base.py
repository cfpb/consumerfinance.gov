from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import Utils

import sys

# DEFAULT VALUES
default_driver_wait = 10

# ELEMENT ID'S FOR TEXTBOXES
EMAIL = "email"

# ELEMENT ID'S FOR BUTTONS


# XPATH LOCATORS
EMAIL_LBL = "//form[@id='signup']/p"
SIGNUP = "//button[text()='Sign up']"


class Base(object):
    def __init__(self, logger, results_folder, base_url=r'http://localhost/',
                 driver=None, driver_wait=default_driver_wait, delay_secs=0):
        if driver is None:
            raise RuntimeError('Driver is invalid or was not provided.')

        self.driver_wait = driver_wait
        self.base_url = base_url
        self.driver = driver
        self.chain = ActionChains(self.driver)
        self.logger = logger
        self.utils = Utils(delay_secs)
        self.results_folder = results_folder

    def go(self, relative_url=''):
        full_url = self.utils.build_url(self.base_url, relative_url)
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

    # Switch to the tab specified by relative_url
    # And return the page title
    def switch_to_new_tab(self, relative_url):
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
            # Wait for the URL to display in the address bar
            WebDriverWait(self.driver, 10)\
                .until(lambda s: len(s.current_url) > 1)

            self.logger.info("Current url: %s" % self.driver.current_url)
            if relative_url in (self.driver.current_url):
                return self.driver.title
                self.driver.close()
                break

        return relative_url + " tab not found!"

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

    # EMAIL SIGNUP
    def set_email_address(self, email_address):
        element = self.driver.find_element_by_id(EMAIL)
        element.send_keys(email_address)

    def click_signup_button(self):
        element = self.driver.find_element_by_xpath(SIGNUP)
        element.click()

    def get_email_label(self):
        # Wait for the label to display
        try:
            element = WebDriverWait(self.driver, self.driver_wait)\
                .until(EC.visibility_of_element_located((By.XPATH,
                                                         EMAIL_LBL)))
            return element.text
        except TimeoutException:
            return "Element NOT found!"

    def is_multiple_email_labels(self):
        l_wait = 5
        # If the list has > 1 elements then multiple labels are displayed
        try:
            WebDriverWait(self.driver, l_wait)\
                .until(lambda s: len(s.find_elements(By.XPATH, EMAIL_LBL)) > 1)
            return True
        except TimeoutException:
            return False

    def is_sign_button_visible(self):
        l_wait = 2
        # If the list has > 1 elements then multiple labels are displayed
        try:
            WebDriverWait(self.driver, l_wait)\
                .until(lambda s: s.find_elements(By.XPATH, SIGNUP))
            return True
        except TimeoutException:
            return False
