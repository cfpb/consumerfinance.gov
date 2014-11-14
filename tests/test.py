import nose
import os
from nose.plugins.attrib import attr
from flask import Flask

from selenose.cases import SeleniumTestCase

from selenium import webdriver
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


from flask.ext.testing import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .test_helpers import *

from sheer.wsgi import app_with_config

class NewsroomTestCase(LiveServerTestCase):

    def create_app(self):
        # Setup server
        config = {'debug': True, 
                  'index': 'cfgov_test', 
                  'elasticsearch': [{'host': 'localhost', 'port': 9200}], 
                  'location': os.getcwd()}
        application = app_with_config(config)
        application.config['TESTING'] = True
        application.config['LIVESERVER_PORT'] = 7000
        return application

    def setUp(self):
        es = Elasticsearch()
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:7000/newsroom/')
        self.filter_dropdown_button = self.driver.find_element_by_xpath('//button[contains(text(), "Filter posts")]')
        click_filter_posts(self)

    def test_filter_display_button(self):
        filter_options = self.driver.find_element_by_class_name('padded-container')


    @attr('checkbox')
    def test_filter_checkboxes(self):
        categoryList = ["Op-Ed", "Press Release", "Speech", "Testimony", "Blog"]
        for cat in categoryList:
            # use this after view changes value of checkbox input to 'Blog'
            # checkbox = self.driver.find_element_by_xpath('//label/input[@value=\"'+ cat +'\"]/..')
            checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), \"'+ cat +'\")]/..')
            checkbox.click()
            assert "is-checked" in checkbox.get_attribute('class')
            checkbox.click()
            assert "is-checkedFocus" in checkbox.get_attribute('class')

    @attr('search')
    @attr('category')
    def test_filter_category_search(self):
        categoryList = ["Op-Ed", "Press Release", "Speech", "Testimony"] # No Blog posts yet so add in when data is there
        for cat in categoryList:
            click_filter_posts(self)
            # checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), \"'+ cat +'\")]/..')
            checkbox = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//label/span[contains(text(), \"'+ cat +'\")]/..'))
            )
            checkbox.click()
            filter_results_button = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//input[@value="Apply filters"]'))
            )
            filter_results_button.click()
            cat = coerce_category_for_dom(cat)
            cat_type_elem = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//a[@href="?filter_category='+ cat +'"]'))
            )
            assert cat_type_elem
            click_filter_posts(self)
            cat = coerce_category_for_dom(cat)
            # checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), \"'+ cat +'\")]/..')
            checkbox = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//label/span[contains(text(), \"'+ cat +'\")]/..'))
            )
            checkbox.click()

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
   nose.main()
