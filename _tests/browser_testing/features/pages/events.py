from pages.base import Base

# CSS SELECTORS
INDIVIDUAL_EVENT_ON_EVENTS_PAGE = 'post-preview__event'
EVENT_DATE = 'span.event-meta_date'
EVENT_TIME = 'span.event-meta_time'
EVENT_LOCATION = 'p.event-meta_address'
EVENT_TAGS = 'li.tags_tag'
TAG_BULLET = 'tags_bullet'
TAG_LINK = 'tags_link'

# XPATH LOCATORS
EVENT_METADATA_PARENT = '//h1[@class="summary_heading"][contains(text(), "event_name")]/../../../..'
EVENT_TITLE_LINK = '//h1[contains(text(), "link_text")]'

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
            INDIVIDUAL_EVENT_ON_EVENTS_PAGE)
        )
        return results_num

    def get_event(self, event_name):
        event = self.driver.find_element_by_xpath(
            EVENT_METADATA_PARENT.replace('event_name', event_name)
        )
        return event

    def get_tags(self, event_name):
        event = self.get_event(event_name)
        tags = event.find_elements_by_css_selector(
            EVENT_TAGS
        )
        tag_list = []
        for tag in tags:
            
            # Had to remove a bullet and a newline from the tag text
            bullet = tag.find_element_by_class_name(TAG_BULLET).text
            tag_text = tag.find_element_by_class_name(TAG_LINK).text
            tag_clean = tag_text.replace(bullet, '').replace('\n', '')
            tag_list.append(tag_clean)
        return tag_list

    def get_location(self, event_name):
        event = self.get_event(event_name)
        location = event.find_element_by_css_selector(
            EVENT_LOCATION
        )
        return location.text

    def get_date(self, event_name):
        event = self.get_event(event_name)
        date = event.find_element_by_css_selector(
            EVENT_DATE
        )
        return date.text

    def get_time(self, event_name):
        event = self.get_event(event_name)
        time = event.find_element_by_css_selector(
            EVENT_TIME
        )
        return time.text

    def click_event_title(self, link_text):
        link = self.driver.find_element_by_xpath(
            EVENT_TITLE_LINK.replace('link_text', link_text)
        )

        # scroll the element into view so it can be
        # observed with SauceLabs screencast
        script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(script, link)
        link.click()