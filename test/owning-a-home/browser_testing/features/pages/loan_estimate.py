from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from pages.base import Base

import re


class LoanEstimate(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(LoanEstimate, self).__init__(logger, directory, base_url,
                                           driver, driver_wait, delay_secs)

    # check that element(s) is on the page
    # @return: element or elements if there are many
    def _element_found(self, css_selector):
        try:
            elements = self.driver.find_elements_by_css_selector(css_selector)
            if len(elements) == 1:
                return elements[0]
            else:
                return elements
        except NoSuchElementException:
            return []

    def tab_is_found(self, tab_name):
        tab_css_selector = '.tab-link__%s' % tab_name.lower()
        if self._element_found(tab_css_selector):
            return True
        return False

    def content_image_is_loaded(self):
        image_css_selector = '.image-map_image'
        images = self._element_found(image_css_selector)
        for image in images:
            if not image.is_displayed():
                next
            if image:
                size = image.size
                if size['width'] > 200 and size['height'] > 200:
                    return True
        return False

    def resize_to_mobile_size(self):
        self.driver.set_window_size(360, 640)

    def expandable_explainers_are_loaded(self, tab_name):
        parent_css_selector = 'div.expandable__form-explainer-%s' % tab_name.lower()
        elements = self._element_found(parent_css_selector)
        good_elements = 0
        for element in elements:
            content_css_selector = '#%s .expandable_content' % element.get_attribute(
                'id')
            if element.is_displayed() and\
                    self._expandable_explainer_content_is_loaded(content_css_selector, element):
                good_elements += 1
        return good_elements

    def _expandable_explainer_content_is_loaded(self, css_selector, parent_element):
        element = self._element_found(css_selector)
        if not element:
            return False
        original_visibility = element.is_displayed()
        ActionChains(self.driver).move_to_element(parent_element).perform()
        parent_element.click()
        # time.sleep(1)
        new_visibility = element.is_displayed()
        return original_visibility != new_visibility

    def _click_tab(self, tab_name):
        css_selector = '.tab-link__%s' % tab_name.lower()
        self.driver.find_element_by_css_selector(css_selector).click()

    def _element_size(self, css_selector):
        element = self._element_found(css_selector)
        item = element
        if type(element) is list:
            for el in element:
                if el.is_displayed():
                    item = el
        if item and item.size:
            return item.size
        return {'width': 0, 'height': 0}

    def hover_an_overlay(self):
        bad_elements = 0
        elements = self._element_found('a.image-map_overlay')
        for element in elements:
            if element.is_displayed():
                ActionChains(self.driver).move_to_element(element).perform()
                anchor = element.get_attribute('href')
                anchor = re.sub('^[^#]*', '', anchor)
                explainer_element = self._element_found(anchor)
                if not explainer_element:
                    bad_elements += 1
                else:
                    classes = filter(lambda x: x,
                                     explainer_element.get_attribute('class').split(' '))
                    if 'has-attention' not in classes:
                        bad_elements += 1

        return bad_elements
