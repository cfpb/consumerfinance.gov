from pages.base import Base

# CSS SELECTORS
INDIVIDUAL_EVENT_ON_EVENTS_PAGE = 'post-preview__event'

# XPATH LOCATORS
EVENT_METADATA_PARENT = '//h1[@class="summary_heading"][contains(text(), "event_name")]/..'
EVENT_DATE = './/span[@class="event-meta_date"]'

class Events(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(Events, self).__init__(logger, directory, base_url,
                                          driver, driver_wait, delay_secs)
        self.logger = logger
        self.driver_wait = driver_wait

    # Get the total number of individual events on the page
    def get_results_number(self):
        results_num = len(self.driver.find_elements_by_class_name(
            'post-preview__event'))
        return results_num

    def get_tags(self, event_name):

        pass

    def get_location(self, event_name):
        pass

    def get_date(self, event_name):
        event = self.driver.find_element_by_xpath(
            EVENT_METADATA_PARENT.replace('event_name', event_name)
        )
        date = event.find_element_by_xpath(
            EVENT_DATE
        )
        return date

    def get_time(self, event_name):
        pass