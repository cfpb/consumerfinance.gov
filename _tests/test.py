import nose
import os
from nose.plugins.attrib import attr
from flask import Flask

from selenium import webdriver
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


from flask.ext.testing import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .test_helpers import *

from sheer.wsgi import app_with_config

class NewsroomTestCase(LiveServerTestCase):

    def create_app(self):
        # Setup server
        config = {'debug': False, 
                  'index': 'cfgov_test', 
                  'elasticsearch': [{'host': 'localhost', 'port': 9200}], 
                  'location': os.getcwd()}
        application = app_with_config(config)
        application.config['LIVESERVER_PORT'] = 31337
        return application

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1400, 850)
        self.driver.get('http://localhost:31337/newsroom/')
        self.filter_dropdown_button = self.driver.find_element_by_xpath('//button[contains(text(), "Filter posts")]')
        click_filter_posts(self)

    def test_filter_display_button(self):
        filter_posts_display_button = self.driver.find_element_by_xpath(
            '//button[contains(text(), "Filter posts")]'
        )
        assert filter_posts_display_button.is_displayed()


    @attr('checkbox')
    def test_filter_checkboxes(self):
        category_list = ["Op-Ed", "Press Release"]
        for cat in category_list:
            checkbox = self.driver.find_element_by_xpath(
                '//label/span[contains(text(), "{0}")]/..'.format(cat))
            checkbox.click()
            assert "is-checked" in checkbox.get_attribute('class')
            checkbox.click()
            assert "is-checkedFocus" in checkbox.get_attribute('class')

    @attr('search')
    @attr('category')
    def test_filter_category_search(self):
        category_list = ["Op-Ed", "Press Release"]
        for cat in category_list:
            click_filter_posts(self)
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//label/span[contains(text(), "{0}")]/..'.format(cat)))
            )
            checkbox.click()
            filter_results_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//input[@value="Apply filters"]'))
            )
            filter_results_button.click()
            cat = coerce_category_for_dom(cat)
            cat_type_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//a[@href="?filter_category={0}"]'.format(cat)))
            )
            assert cat_type_elem
            click_filter_posts(self)
            cat = coerce_category_for_dom(cat)
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//label/span[contains(text(), "{0}")]/..'.format(cat)))
            )
            checkbox.click()

    @attr('search')
    @attr('topics')
    def test_filter_topic_search(self):
        topic_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//input[@value="Search for topics"]'
            ))
        )
        topic_input.click()
        topic_input.send_keys("for")
        topic_choice_results = self.driver.find_element_by_xpath(
            '//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]'
        )
        assert topic_choice_results.is_displayed()
        choice = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"For")]/..'
            ))
        )
        choice.click()
        topic_elem = self.driver.find_element_by_xpath(
            '//div[@id="filter_tags_chosen"]/ul/li/span[contains(text(), "Foreclosure")]'
        )
        assert topic_elem

    @attr('search')
    @attr('authors')
    def test_filter_author_search(self):
        author_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//input[@value="Search for authors"]'
            ))
        )
        author_input.click()
        author_input.send_keys("bat")
        author_choice_results = self.driver.find_element_by_xpath(
            '//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]'
        )
        assert author_choice_results.is_displayed()
        choice = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"Bat")]/..'
            ))
        )
        choice.click()
        author_elem = self.driver.find_element_by_xpath(
            '//div[@id="filter_author_chosen"]/ul/li/span[contains(text(), "Batman")]'
        )
        assert author_elem
        filter_results_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//input[@value="Apply filters"]'
            ))
        )
        filter_results_button.click()
        author = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//p[@class="summary_byline"][contains(text(), "Bat")]'
            ))
        )
        assert author

    @attr('search')
    @attr('date')
    def test_filter_date_search(self):
        # scroll(self.driver)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, 
                '//div[@id="filter_range_date_gte-replacement"]/div[1]'
            ))
        )
        
        # click 'from month'
        self.driver.find_element_by_xpath(
            '//select[@id="filter_from_month"]/option[@value="01"]'
        ).click() 
        # click 'from year'
        self.driver.find_element_by_xpath(
            '//select[@id="filter_from_year"]/option[@value="2013"]'
        ).click()
        
        # click 'to month'
        self.driver.find_element_by_xpath(
            '//select[@id="filter_to_month"]/option[@value="02"]'
        ).click()
        # click 'to year'
        self.driver.find_element_by_xpath(
            '//select[@id="filter_to_year"]/option[@value="2013"]'
        ).click()

        # Search
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, '//input[@value="Apply filters"]'
            ))
        ).click()

        filtered_article_date = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                '//div[@id="pagination_content"]/article[1]/div[1]/span[1]'
            ))
        )
        filtered = 'jan' in filtered_article_date.text.lower() or 'feb' in filtered_article_date.text.lower()
        assert filtered

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
   nose.main()
