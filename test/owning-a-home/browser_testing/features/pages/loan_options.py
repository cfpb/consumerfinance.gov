# coding: utf-8
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base

# HREF FOR INTERNAL  LINKS
CONVENTIONAL_LOAN = "./conventional-loans"
FHA_LOAN = "./FHA-loans"
SPECIAL_LOAN = "./special-loan-programs"

# HREF FOR RELATED  LINKS
RELATED_FHA_LOAN = "../FHA-loans/"
RELATED_SPECIAL = "../special-loan-programs/"
RELATED_CONV = "../conventional-loans/"

# ELEMENTS ID
LOAN_AMOUNT = "loan-amount-value"
INTEREST_RATE = "loan-interest-value"

# ELEMENT CSS SELECTOR
ELT = "#expandable__loan-term"
LOAN_TERM_EXPAND = ELT + " .expandable_cue-open .expandable_cue_text"
LOAN_TERM_COLLAPSE = ELT + " .expandable_cue-close .expandable_cue_text"
LOAN_TERM_SUBSECTION = ELT + " .expandable_content"

EIR = "#expandable__interest-rate "
INTEREST_RATE_EXPAND = EIR + ".expandable_cue-open .expandable_cue_text"
INTEREST_RATE_COLLAPSE = EIR + ".expandable_cue-close .expandable_cue_text"
INTEREST_RATE_SUBSECTION = EIR + ".expandable_content"

ELE = "#expandable__loan-type "
LOAN_TYPE_EXPAND = ELE + ".expandable_cue-open .expandable_cue_text"
LOAN_TYPE_COLLAPSE = ELE + ".expandable_cue-close .expandable_cue_text"
LOAN_TYPE_SUBSECTION = ELE + ".expandable_content"

SELECTED_TERM = ".term-timeline a.current .loan-length"


class LoanOptions(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(LoanOptions, self).__init__(logger, directory, base_url,
                                          driver, driver_wait, delay_secs)
        self.logger = logger
        self.driver_wait = driver_wait

    def click_learn_more(self, page_section):
        l_wait = 2  # Local Wait

        if(page_section == 'Loan term'):
            e_expand = LOAN_TERM_EXPAND
            e_collapse = LOAN_TERM_COLLAPSE
        elif(page_section == 'Interest rate type'):
            e_expand = INTEREST_RATE_EXPAND
            e_collapse = INTEREST_RATE_COLLAPSE
        elif(page_section == 'Loan type'):
            e_expand = LOAN_TYPE_EXPAND
            e_collapse = LOAN_TYPE_COLLAPSE
        else:
            raise Exception(page_section + " is NOT a valid section")

        # If the collapse link is visible,
        # Then the Learn More pane is already expanded
        try:
            msg = 'Element %s not found after %s secs' % (e_collapse, l_wait)
            WebDriverWait(self.driver, l_wait).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, e_collapse)), msg)

        except TimeoutException:
            e = self.driver.find_element_by_css_selector(e_expand)
            # scroll the element into view so it can be
            # observed with SauceLabs screencast
            script = "arguments[0].scrollIntoView(true);"
            self.driver.execute_script(script, e)
            e.click()

        # Wait for the collapse button to appear
        msg = 'Element %s not found after %s secs' % (e_collapse,
                                                      self.driver_wait)
        WebDriverWait(self.driver, self.driver_wait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, e_collapse)), msg)

    def click_collapse(self, page_section):
        if(page_section == 'Loan term'):
            e_css = LOAN_TERM_COLLAPSE
            # e_expand = LOAN_TERM_EXPAND
        elif(page_section == 'Interest rate type'):
            e_css = INTEREST_RATE_COLLAPSE
            # e_expand = INTEREST_RATE_EXPAND
        elif(page_section == 'Loan type'):
            e_css = LOAN_TYPE_COLLAPSE
            # e_expand = LOAN_TYPE_EXPAND
        else:
            raise Exception(page_section + " is NOT a valid section")

        msg = 'Element %s not found after %s secs' % (e_css, self.driver_wait)
        # Wait for the collapse button to appear before clicking it
        element = WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, e_css)), msg)

        element.click()

    # this method clicks the 'Get all the details' link
    # for the 'loan_type' specified
    def click_loan_type(self, loan_type):
        if(loan_type == 'Conventional'):
            e_href = CONVENTIONAL_LOAN
        elif(loan_type == 'FHA'):
            e_href = FHA_LOAN
        elif(loan_type == 'Special programs'):
            e_href = SPECIAL_LOAN
        else:
            raise Exception(loan_type + " is NOT a valid Loan Type")

        e_text = "Get all the details"
        e_xpath = "//a[text() = '" + e_text + "' and @href='" + e_href + "']"

        msg = 'Element %s not found after %s sec' % (e_xpath, self.driver_wait)

        element = WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.element_to_be_clickable((By.XPATH, e_xpath)), msg)

        # scroll the element into view so it can be
        # observed with SauceLabs screencast
        script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(script, element)

        element.click()

    def click_go_link(self, loan_type):
        if(loan_type == 'FHA'):
            e_href = RELATED_FHA_LOAN
        elif(loan_type == 'Special Programs'):
            e_href = RELATED_SPECIAL
        elif(loan_type == 'Conventional'):
            e_href = RELATED_CONV
        else:
            raise Exception(loan_type + " is NOT a valid Loan Type")
        e_xpath = "//a[contains(concat(' ', @class, ' '), ' jump-link ')]" \
                  "[@href='" + e_href + "']"
        msg = 'Element %s not found after %s sec' % (e_xpath, self.driver_wait)

        element = WebDriverWait(self.driver, self.driver_wait).until(
            EC.element_to_be_clickable((By.XPATH, e_xpath)), msg)
        element.click()

    def get_subsection_text(self, page_section):
        local_wait = 2

        if(page_section == 'Loan term'):
            e_css = LOAN_TERM_SUBSECTION + " .tight-heading"
        elif(page_section == 'Interest rate type'):
            e_css = INTEREST_RATE_SUBSECTION + " .tight-heading"
        elif(page_section == 'Loan type'):
            e_css = LOAN_TYPE_SUBSECTION + " .tight-heading"
        else:
            raise Exception(page_section + " is NOT a valid section")

        msg = 'Element %s was not found after %s seconds' % (e_css, local_wait)
        try:
            # Wait for the subsection to expand
            element = WebDriverWait(self.driver, local_wait)\
                .until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                         e_css)), msg)
            return element.text
        except TimeoutException:
            return 'Section NOT visible'

    def get_subsection_visibility(self, page_section):
        local_wait = 2

        if(page_section == 'Loan term'):
            e_css = LOAN_TERM_SUBSECTION
        elif(page_section == 'Interest rate type'):
            e_css = INTEREST_RATE_SUBSECTION
        elif(page_section == 'Loan type'):
            e_css = LOAN_TYPE_SUBSECTION
        else:
            raise Exception(page_section + " is NOT a valid section")

        msg = 'Element %s was not found after %s seconds' % (e_css, local_wait)
        try:
            # Wait for the subsection to expand
            element = WebDriverWait(self.driver, local_wait).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, e_css)), msg)
            eVisibility = element.get_attribute("aria-expanded")
            return "element %s visible = %s" % (page_section, eVisibility)
        except TimeoutException:
            return msg

    def get_expand_button_caption(self, page_section):
        if(page_section == 'Loan term'):
            e_css = LOAN_TERM_COLLAPSE
        elif(page_section == 'Interest rate type'):
            e_css = INTEREST_RATE_COLLAPSE
        elif(page_section == 'Loan type'):
            e_css = LOAN_TYPE_COLLAPSE
        else:
            raise Exception(page_section + " is NOT a valid section")

        caption = self.driver.find_element_by_css_selector(e_css).text
        return caption

    def get_loan_amount(self):
        element = self.driver.find_element_by_id(LOAN_AMOUNT)
        return element.get_attribute("placeholder")

    def get_interest_rate(self):
        element = self.driver.find_element_by_id(INTEREST_RATE)
        return element.get_attribute("placeholder")

    def get_loan_term(self):
        element = self.driver.find_element_by_css_selector(SELECTED_TERM)
        return element.get_attribute("innerText")
