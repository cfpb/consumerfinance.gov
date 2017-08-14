# coding: utf-8
from selenium.common.exceptions import NoSuchElementException

from pages.base import Base


# Navigation header CSS selector
NAVBAR = ".process-nav_header"


class Journey(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(Journey, self).__init__(logger, directory, base_url,
                                      driver, driver_wait, delay_secs)

    def is_navbar_found(self):
        try:
            self.driver.find_element_by_css_selector(NAVBAR)
            return True
        except NoSuchElementException:
            return False
