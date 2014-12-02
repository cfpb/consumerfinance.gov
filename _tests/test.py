import nose
import os
import datetime
from nose.plugins.attrib import attr
from selenium import webdriver
from flask.ext.testing import LiveServerTestCase

from .test_helpers import *
from sheer.wsgi import app_with_config

SAUCE_TESTING = os.environ.get('SAUCE_TESTING')
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

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
        if SAUCE_TESTING:
            desired_capabilities = {
                'name': os.getenv('SELENIUM_NAME',
                                  'cfgov-refresh browser tests ') + str(datetime.datetime.now()),
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
            sauce_url = "http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub".format(SAUCE_USERNAME,
                                                                                 SAUCE_ACCESS_KEY)
            self.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=sauce_url)
        else:
            self.driver = webdriver.Chrome()
        
        self.driver.set_window_size(1400, 850)
        self.driver.implicitly_wait(10)
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
			checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "'+ cat +'")]/..')
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
			checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "'+ cat +'")]/..')
			checkbox.click()
			filter_results_button = self.driver.find_element_by_xpath('//input[@value="Apply filters"]')
			filter_results_button.click()
			cat = coerce_category(cat)
			cat_type_elem = self.driver.find_element_by_xpath('//a[@href="?filter_category='+ cat +'"]')
			assert cat_type_elem
			results_num = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_header"]')
			if cat == "Op-Ed":
				assert "14" in results_num.text
			elif cat == "Press Release":
				assert "5" in results_num.text
			click_filter_posts(self)
			cat = coerce_category(cat)
			checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "'+ cat +'")]/..')
			checkbox.click()

	@attr('search')
	@attr('topic')
	def test_filter_topic_search(self):
		topic_input = self.driver.find_element_by_xpath('//input[@value="Search for topics"]')
		topic_input.click()
		topic_input.send_keys("for")
		topic_choice_results = self.driver.find_element_by_xpath(
			'//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]'
		)
		assert topic_choice_results.is_displayed()
		choice = self.driver.find_element_by_xpath('//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"For")]/..')
		choice.click()
		topic_elem = self.driver.find_element_by_xpath(
			'//div[@id="filter_tags_chosen"]/ul/li/span[contains(text(), "Foreclosure")]'
		)
		assert topic_elem
		self.driver.find_element_by_xpath('//input[@value="Apply filters"]').click()
		results_num = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_header"]')
		results_filter = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_filter"]')
		assert "5" in results_num.text
		assert "Foreclosure" in results_filter.text


	@attr('search')
	@attr('author')
	def test_filter_author_search(self):
		author_input = self.driver.find_element_by_xpath('//input[@value="Search for authors"]')
		author_input.click()
		author_input.send_keys("bat")
		author_choice_results = self.driver.find_element_by_xpath(
			'//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]'
		)
		assert author_choice_results.is_displayed()
		choice = self.driver.find_element_by_xpath('//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"Bat")]/..')
		choice.click()
		author_elem = self.driver.find_element_by_xpath(
			'//div[@id="filter_author_chosen"]/ul/li/span[contains(text(), "Batman")]'
		)
		assert author_elem
		filter_results_button = self.driver.find_element_by_xpath('//input[@value="Apply filters"]')
		filter_results_button.click()
		author = self.driver.find_element_by_xpath('//p[@class="summary_byline"][contains(text(), "Bat")]')
		assert author
		results_num = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_header"]')
		results_filter = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_filter"]')
		assert "14" in results_num.text
		assert "Batman" in results_filter.text

	@attr('search')
	@attr('date')
	def test_filter_date_search(self):
		self.driver.find_element_by_xpath('//div[@class="input-group_item custom-select is-enabled"]')
		
		# click 'from month'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-month"]/option[@value="01"]'
		).click() 
		# click 'from year'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-year"]/option[@value="2011"]'
		).click()
		
		# click 'to month'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-month"]/option[@value="02"]'
		).click()
		# click 'to year'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-year"]/option[@value="2011"]'
		).click()

		# Search
		self.driver.find_element_by_xpath('//input[@value="Apply filters"]').click()

		results_num = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_header"]')
		results_filter = self.driver.find_element_by_xpath('//li[@class="list_item filtered-by_filter"]')
		filtered_article_date = self.driver.find_element_by_xpath('//div[@id="pagination_content"]/article[1]/div[1]/span[1]')
		
		filtered = 'jan' in filtered_article_date.text.lower() or 'feb' in filtered_article_date.text.lower()
		assert filtered
		assert '9' in results_num.text
		assert 'January 2011' in results_filter.text
		assert 'February 2011' in results_filter.text

	@attr('clear')
	def test_clear_filters_button(self):
		category_list = ["Op-Ed", "Press Release"]
		for cat in category_list:
			checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "'+ cat +'")]/..')
			checkbox.click()
			assert "is-checked" in checkbox.get_attribute('class')
		topic_input = self.driver.find_element_by_xpath('//input[@value="Search for topics"]')
		topic_input.click()
		topic_input.send_keys("for")
		topic_choice_results = self.driver.find_element_by_xpath(
			'//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]'
		)
		assert topic_choice_results.is_displayed()
		choice = self.driver.find_element_by_xpath( 
				'//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"For")]/..'
		)
		choice.click()
		topic_elem = self.driver.find_element_by_xpath(
			'//div[@id="filter_tags_chosen"]/ul/li/span[contains(text(), "Foreclosure")]'
		)
		assert topic_elem
		author_input = self.driver.find_element_by_xpath('//input[@value="Search for authors"]')
		author_input.click()
		author_input.send_keys("bat")
		author_choice_results = self.driver.find_element_by_xpath(
			'//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]'
		)
		assert author_choice_results.is_displayed()
		choice = self.driver.find_element_by_xpath('//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"Bat")]/..')
		choice.click()
		author_elem = self.driver.find_element_by_xpath(
			'//div[@id="filter_author_chosen"]/ul/li/span[contains(text(), "Batman")]'
		)
		assert author_elem

		# click 'from month'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-month"]/option[@value="01"]'
		).click() 
		# click 'from year'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-year"]/option[@value="2011"]'
		).click()
		
		# click 'to month'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-month"]/option[@value="02"]'
		).click()
		# click 'to year'
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-year"]/option[@value="2011"]'
		).click()

		self.driver.find_element_by_xpath('//input[@value="Apply filters"]').click()
		click_filter_posts(self)
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-month"]/option[@value="01"]'
		).is_selected() 
		self.driver.find_element_by_xpath(
			'//select[@id="filter_from-year"]/option[@value="2011"]'
		).is_selected()		
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-month"]/option[@value="02"]'
		).is_selected()
		self.driver.find_element_by_xpath(
			'//select[@id="filter_to-year"]/option[@value="2011"]'
		).is_selected()

		self.driver.find_element_by_xpath('//input[@value="Clear filters"]').click()
		for cat in category_list:
			checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "'+ cat +'")]/..')
			unchecked = not "is-checked" in checkbox.get_attribute('class')
			assert unchecked
		self.driver.implicitly_wait(0)
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_tags_chosen"]/ul/li[@class="search-choice"]')) == 0
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_author_chosen"]/ul/li[@class="search-choice"]')) == 0
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_from-month"]/option[@selected="selected"]')) == 0
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_from-year"]/option[@selected="selected"]')) == 0
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_to-month"]/option[@selected="selected"]')) == 0
		assert len(self.driver.find_elements_by_xpath('//div[@id="filter_to-year"]/option[@selected="selected"]')) == 0

	@attr('pagination')
	def test_pagination_display(self):
		self.driver.find_element_by_xpath('//label/span[contains(text(), "Op-Ed")]/..').click()
		self.driver.find_element_by_xpath('//input[@value="Apply filters"]')
		assert self.driver.find_element_by_xpath('//nav[@class="post-pagination pagination"]/..').is_displayed()
		
		click_filter_posts(self)
		self.driver.find_element_by_xpath('//label/span[contains(text(), "Op-Ed")]/..').click()
		self.driver.find_element_by_xpath('//label/span[contains(text(), "Press Release")]/..').click()
		self.driver.find_element_by_xpath('//input[@value="Apply filters"]').click()
		self.driver.implicitly_wait(0)
		assert len(self.driver.find_elements_by_xpath('//nav[@class="post-pagination pagination"]/..')) == 0

	@attr('pagination')
	def test_pagination_form(self):
		next = self.driver.find_element_by_xpath('//a[@class="btn btn__super pagination_next"]')
		scroll_to_element(self.driver, next)
		next.click()
		current_page_input = self.driver.find_element_by_id('pagination_current-page')
		assert current_page_input.get_attribute('value') == '2'

		prev = self.driver.find_element_by_xpath('//a[@class="btn btn__super pagination_prev"]')
		scroll_to_element(self.driver, prev)
		prev.click()
		current_page_input = self.driver.find_element_by_id('pagination_current-page')
		assert current_page_input.get_attribute('value') == '1'

		self.driver.execute_script("window.document.getElementById('pagination_current-page').value = 2;")
		self.driver.find_element_by_id('pagination_submit').click()
		scroll_to_element(self.driver, self.driver.find_element_by_id('pagination_submit'))
		current_page_input = self.driver.find_element_by_id('pagination_current-page')
		assert current_page_input.get_attribute('value') == '2'

	def tearDown(self):
		self.driver.close()

if __name__ == '__main__':
   nose.main()
