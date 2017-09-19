from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utils import *

__author__ = 'CFPBLabs'


class Website(object):
    def __init__(self, base_url=r'http://localhost/', driver=None, delay_secs=0):
        if driver is None:
            assert 'Driver is invalid or was not provided.'

        self.utils = Utils(delay_secs)
        self.base_url = base_url
        self.driver = driver
        self.chain = ActionChains(self.driver)

    def go(self, relative_url=''):
        full_url = self.utils.build_url(self.base_url, relative_url)
        self.driver.get(full_url)

    def home(self):
        self.go(self.utils.home_url)

    def open_menu_item(self, menu_item):
        self.utils.zzz()
        element = self.driver.find_element_by_link_text(menu_item)
        element.click()  # not sure why we have to click here
        self.chain.move_to_element(element)  # hover

    def open_submenu_link(self, sub_menu_link):
        self.utils.zzz()
        link = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_link_text(sub_menu_link))
        link.click()

    def open_footer_link(self, footer_link):
        self.utils.zzz()
        # ToDo: ensure that we start from the footer
        footer = self.driver
        link = WebDriverWait(footer, 5).until(lambda footer: footer.find_element_by_link_text(footer_link))
        link.click()

    def click_link(self, link_text):
        self.utils.zzz()
        link = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_link_text(link_text))
        link.click()

    def click_image_by_id(self, image_id):
        self.utils.zzz()
        image = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id(image_id))
        image.click()

    def search_and_select_first_from_drop_list(self, element_nickname, entered_text):
        self.utils.zzz()
        # convert nickname into an element id
        element_id = self.utils.convert_nickname_to_id(element_nickname)
        element = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id(element_id))
        element.click()

        search_box = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_css_selector(".chzn-search input"))
        search_box.click()

        search_box.send_keys(entered_text)
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.ENTER)

    def search_and_select_link_from_autocomplete(self, element_nickname, entered_text, link_text):
        self.utils.zzz()
        # convert nickname into an element id
        element_id = self.utils.convert_nickname_to_id(element_nickname)
        search_box = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id(element_id))
        search_box.click()
        search_box.send_keys(entered_text)

        # Give autocomplete 1 second.
        self.utils.zzz(1)
        link = WebDriverWait(self.driver, 5).until(lambda driver : driver.find_element_by_link_text(link_text))
        link.click()



    def enter_text(self, element_id, entered_text):
        self.utils.zzz()
        # Sends keys to an element by id.
        element = WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id(element_id))
        element.send_keys(entered_text)

    def close_browser(self):
        self.driver.quit()

    # Evaluation Helpers
    def get_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    def get_footer(self,tag_name="footer"):
        return self.driver.find_element_by_tag_name(tag_name)

    def save_screenshot(self, filename=''):
        if filename == '':
            filename = 'screenshot'
        # ToDo: write util to build proper screenshot file path based on config
        full_path = '%s/%s.%s' % ('./test-results', filename, 'png')

        self.driver.save_screenshot(full_path) # This saves the 'screenshot'

    # Assertion Helpers
    def is_text_in_body(self, text):
        try:
            # look in the body of the page
            element = self.driver.find_element_by_tag_name("body")
        except NoSuchElementException, e:
            return False

        return text in element.text

    def is_text_last_in_breadcrumb(self, text):
        # ToDo: look in the breadcrumb
        return self.is_text_in_body(text)

    # compare expected to actual current url
    def is_url_current(self, expected_url):
        self.utils.zzz()
        return expected_url == self.get_url()

    # compare expected to actual title
    def is_title(self, expected_title):
        self.utils.zzz()
        return expected_title == self.get_title()

    def is_page_properly_loaded(self):
        self.utils.zzz()
        # ToDo: fully verify and validate that the page loaded properly

        # There shouldn't be a 'ERROR 404 - PAGE NOT FOUND' message
        message = 'ERROR 404 - PAGE NOT FOUND'
        if self.is_text_in_body(message):
            return False

        return True

