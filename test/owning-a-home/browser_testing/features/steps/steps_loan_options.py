# coding: utf-8
from behave import then, when
from hamcrest.core import assert_that, equal_to
from hamcrest.library.text.stringcontains import contains_string


# EXPAND/COLLAPSE
@when(u'I click Learn More to expand the "{section_name}" section')
def step(context, section_name):
    context.loan_options.click_learn_more(section_name)


@when(u'I collapse the "{section_name}" section')
def step(context, section_name):
    context.loan_options.click_collapse(section_name)


@then(u'I should see a collapse link for the "{section_name}" section')
def step(context, section_name):
    caption = context.loan_options.get_expand_button_caption(section_name)
    assert_that(caption, contains_string('Collapse'))


# SUB-SECTIONS
@then(u'I should see "{expected_text}" inside the "{section_name}" section')
def step(context, expected_text, section_name):
    actual_text = context.loan_options.get_subsection_text(section_name)
    assert_that(actual_text, equal_to(expected_text))


@then(u'I should NOT see the "{section_name}" section expanded')
def step(context, section_name):
    actual_text = context.loan_options.get_subsection_visibility(section_name)
    expected_state = "element " + section_name + " visible = false"
    assert_that(actual_text, equal_to(expected_state))


@then(u'I should see "{loan_amount}" as the default loan amount')
def step(context, loan_amount):
    actual_value = context.loan_options.get_loan_amount()
    assert_that(actual_value, equal_to(loan_amount))


@then(u'I should see "{interest_rate}" as the default interest rate')
def step(context, interest_rate):
    actual_value = context.loan_options.get_interest_rate()
    assert_that(actual_value, equal_to(interest_rate))


@then(u'I should see "{loan_term}" years as the default loan term')
def step(context, loan_term):
    actual_term = context.loan_options.get_loan_term()
    assert_that(actual_term, equal_to(loan_term))


# Choosing the right loan type
@when(u'I click Get all the details for "{loan_type}" loans')
def step(context, loan_type):
    context.loan_options.click_loan_type(loan_type)


# OTHER LOAN TYPES
@when(u'I click OTHER LOAN TYPES "{loan_type}"')
def step(context, loan_type):
    context.loan_options.click_go_link(loan_type)
