from pages.base import Base

CATEGORIES = ('Op-Ed', 'Press Release')

# CSS SELECTORS
FILTER_PRESSED = 'aria-pressed'
CURRENT_PAGE = 'pagination_current-page'
PAGINATION_SUBMIT = 'pagination_submit'

# XPATH LOCATORS

# FILTER BUTTONS
FILTER_POSTS_BUTTON = '//button[contains(text(), "Filter posts")]'
APPLY_FILTERS_BUTTON = '//input[@value="Apply filters"]'
CLEAR_FILTERS_BUTTON = '//input[@value="Clear filters"]'

# FILTER MISC
CATEGORY_CHECKBOX = '//label/span[contains(text(), "category_name")]/..'
RESULTS_NUMBER = '//li[@class="list_item filtered-by_header"]'
FILTER_USED = '//li[@class="list_item filtered-by_filter"]'

# PAGINATION
PAGINATION = '//nav[@class="post-pagination pagination"]/..'
NEXT_PAGE = '//a[@class="btn btn__super pagination_next"]'
PREVIOUS_PAGE = '//a[@class="btn btn__super pagination_prev"]'

# FILTER DROPDOWNS
FROM_MONTH = '//select[@id="filter_from-month"]/option[@value="from_month"]'
FROM_YEAR = '//select[@id="filter_from-year"]/option[@value="from_year"]'
TO_MONTH = '//select[@id="filter_to-month"]/option[@value="to_month"]'
TO_YEAR = '//select[@id="filter_to-year"]/option[@value="to_year"]'

# CHECK IF FILTERS ARE SELECTED
TAGS_CHOSEN = '//div[@id="filter_tags_chosen"]/ul/li[@class="search-choice"]'
AUTHORS_CHOSEN = '//div[@id="filter_author_chosen"]/ul/li[@class="search-choice"]'
FROM_MONTH_SELECTED = '//div[@id="filter_from-month"]/option[@selected="selected"]'
FROM_YEAR_SELECTED = '//div[@id="filter_from-year"]/option[@selected="selected"]'
TO_MONTH_SELECTED = '//div[@id="filter_to-month"]/option[@selected="selected"]'
TO_YEAR_SELECTED = '//div[@id="filter_to-year"]/option[@selected="selected"]'

# TOPIC/AUTHOR SEARCH
AUTHOR_SEARCH_INPUT = '//input[@value="Search for authors"]'
TOPIC_SEARCH_INPUT = '//input[@value="Search for topics"]'
SELECT_AUTHOR = '//div[@id="filter_author_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"author_name")]/..'
SELECT_TOPIC = '//div[@id="filter_tags_chosen"]/div/ul[@class="chosen-results"]/li/em[contains(text(),"topic_name")]/..'

class Newsroom(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(Newsroom, self).__init__(logger, directory, base_url,
                                          driver, driver_wait, delay_secs)
        self.logger = logger
        self.driver_wait = driver_wait

    def click_apply_filters(self):
        apply_filters_button = self.driver.find_element_by_xpath(
            APPLY_FILTERS_BUTTON
        )
        apply_filters_button.click()

    def click_clear_filters(self):
        clear_filters_button = self.driver.find_element_by_xpath(
            CLEAR_FILTERS_BUTTON
        )
        clear_filters_button.click()

    def click_filter_posts_button(self):
        filter_posts_display_button = self.driver.find_element_by_xpath(
            FILTER_POSTS_BUTTON
        )
        parent_element = self.driver.find_element_by_xpath(
            '{0}/..'.format(FILTER_POSTS_BUTTON)
        )
        if parent_element.get_attribute(FILTER_PRESSED) == 'false':
            filter_posts_display_button.click()
            self.utils.zzz(1)

    def click_category_checkbox(self, category_name):
        checkbox = self.driver.find_element_by_xpath(
            CATEGORY_CHECKBOX.replace('category_name',
                                      category_name
                                      )
        )
        checkbox.click()
    def set_date_filter(self, from_month=None, from_year=None, to_month=None, 
                        to_year=None):
        if from_month:
            from_month = self.driver.find_element_by_xpath(
                FROM_MONTH.replace('from_month', from_month)
            )
            from_month.click()
        if from_year:
            from_year = self.driver.find_element_by_xpath(
                FROM_YEAR.replace('from_year', from_year)
            )
            from_year.click()
        if to_month:
            to_month = self.driver.find_element_by_xpath(
                TO_MONTH.replace('to_month', to_month)
            )
            to_month.click()
        if to_year:
            to_year = self.driver.find_element_by_xpath(
                TO_YEAR.replace('to_year', to_year)
            )
            to_year.click()

    def get_results_number(self):
        results = self.driver.find_element_by_xpath(RESULTS_NUMBER)
        results_num = results.text.split(' ')[0]
        return results_num

    def get_filter_used(self):
        filter_used = self.driver.find_element_by_xpath(FILTER_USED)
        return filter_used.text

    # Check to see if any filters are selected
    def are_filters_selected(self):
        tags = self.driver.find_elements_by_xpath(TAGS_CHOSEN)
        author = self.driver.find_elements_by_xpath(AUTHORS_CHOSEN)
        from_month = self.driver.find_elements_by_xpath(FROM_MONTH_SELECTED)
        from_year = self.driver.find_elements_by_xpath(FROM_YEAR_SELECTED)
        to_month = self.driver.find_elements_by_xpath(TO_MONTH_SELECTED)
        to_year = self.driver.find_elements_by_xpath(TO_YEAR_SELECTED)
        for filter in (tags, author, from_month, from_year, to_month, to_year):
            if len(filter) > 0:
                return True

        for category in CATEGORIES:
            checkbox = self.driver.find_element_by_xpath(
                CATEGORY_CHECKBOX.replace('category_name', category)
            )
            if "is-checked" in checkbox.get_attribute('class'):
                return True
        return False

    def is_category_checked(self, category_name):
        checkbox = self.driver.find_element_by_xpath(
            CATEGORY_CHECKBOX.replace('category_name', category_name)
        )
        return "is-checked" in checkbox.get_attribute('class')

    def is_pagination_displayed(self):
        if len(self.driver.find_elements_by_xpath(PAGINATION)) > 0:
            return True
        return False

    def click_pagination_button(self, button):
        if button == 'next':
            next = self.driver.find_element_by_xpath(NEXT_PAGE)
            next.click()
        elif button == 'previous':
            prev = self.driver.find_element_by_xpath(PREVIOUS_PAGE)
            prev.click()
        else:
            self.driver.execute_script(
                "window.document.getElementById('{0}').value = {1};".format(
                    CURRENT_PAGE, button
                )
            )
            self.driver.find_element_by_id(PAGINATION_SUBMIT).click()

    def get_current_page_number(self):
        self.scroll_to_element(
            self.driver.find_element_by_id(PAGINATION_SUBMIT)
        )
        current_page_input = self.driver.find_element_by_id(CURRENT_PAGE)
        return current_page_input.get_attribute('value')

    def enter_text_into_search_filter(self, filter_type, input_text):
        if filter_type == 'author':
            search_input = self.driver.find_element_by_xpath(AUTHOR_SEARCH_INPUT)
        elif filter_type == 'topic':
            search_input = self.driver.find_element_by_xpath(TOPIC_SEARCH_INPUT)
        search_input.click()
        search_input.send_keys(input_text)

    def select_search_filter(self, filter_type, name):
        if filter_type == 'author':
            choice = self.driver.find_element_by_xpath(
                SELECT_AUTHOR.replace('author_name', name)
                )
        elif filter_type == 'topic':
            choice = self.driver.find_element_by_xpath(
                SELECT_TOPIC.replace('topic_name', name)
                )
        choice.click()
