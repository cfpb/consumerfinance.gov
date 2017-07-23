
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

from pages.base import Base

import requests

# ELEMENT FOR LINKS
LINK_TAG = 'a'


class Navigation(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(Navigation, self).__init__(logger, directory, base_url,
                                         driver, driver_wait, delay_secs)

    def click_link(self, link_text):

        # this is a temporary fix to catch jump-links on loan options
        # page, since their text is wrapped in a span
        # TODO: consider using ids instead
        xpath_text = "//a[contains(text(),'" + link_text + "')]"
        xpath_span = "//a/span[contains(text(),'" + link_text + "')]/.."
        try:
            element = self.driver.find_element_by_xpath(xpath_text)
        except NoSuchElementException:
            element = self.driver.find_element_by_xpath(xpath_span)

        # scroll the element into view so it can be
        # observed with SauceLabs screencast
        script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(script, element)

        # element.click()

        try:
            element.click()
        except WebDriverException:
            action = webdriver.ActionChains(self.driver)\
                .move_to_element_with_offset(element, 0, 20).click()
            action.perform()

    def click_link_with_id(self, link_id):
        element = self.driver.find_element_by_id(link_id)

        # scroll the element into view so it can be
        # observed with SauceLabs screencast
        script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(script, element)
        element.click()

    def check_link_status_code(self, link):
        try:
            r = requests.head(link)
            return r.status_code > 199 and r.status_code < 400
        except requests.ConnectionError:
            return False

    def check_links_for_404s(self, base_url):
        results = []
        link_elements = self.driver.find_elements_by_tag_name(LINK_TAG)
        for elem in link_elements:
            link = elem.get_attribute('href')
            # only print results that aren't localhost links when running locally
            if link and not link.startswith('tel') and not link.startswith('http://localhost') and not self.check_link_status_code(link):
                results.append(link)
                print link
        return results
