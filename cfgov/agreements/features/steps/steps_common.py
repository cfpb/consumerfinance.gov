# coding=utf-8

from behave import given, when, then
from hamcrest import *

__author__ = 'CFPBLabs'

agency_name = 'Consumer Financial Protection Bureau'

# Given statements
# these arrange the conditions of a test


@given(u'I visit the www.consumerfinance.gov homepage')
def step(context):
    context.website.go()


@given(u'I visit the www.consumerfinance.gov/{page_url} URL')
def step(context, page_url):
    context.website.go(page_url)


@given(u'I click on the "{link_text}" link in the footer')
def step(context, link_text):
    context.website.open_footer_link(link_text)


# When statements
# these are action(s) performed as part of the test

@when(u'I click on the CFPB logo image')
def step(context):
    # Click the image with id='logo'
    context.website.click_image_by_id("logo")


@when(u'I click on the "{link_text}" link')
def step(context, link_text):
    context.website.click_link(link_text)


@when(u'I click on the "{link_text}" link in the footer')
def step(context, link_text):
    context.website.open_footer_link(link_text)

# Prototype: I select what I call the "card issuer" drop list and search
# and select "bank of america"


@when(
    u'I select what I call the "{element_nickname}" drop list and search "{entered_text}" and choose first')
def step(context, element_nickname, entered_text):
    context.website.search_and_select_first_from_drop_list(
        element_nickname, entered_text)

# Prototype: I select what I call the "search" text box and search
# "reverse" and choose "What is a reverse mortgage?"


@when(
    u'I select what I call the "{element_nickname}" text box and search "{entered_text}" and choose "{link_text}"')
def step(context, element_nickname, entered_text, link_text):
    context.website.search_and_select_link_from_autocomplete(
        element_nickname, entered_text, link_text)


# Then statements
# these are the assertion(s) that verify/validate that the test did or did
# not pass

@then('I should be directed to the homepage')
def step(context):
    expected_url = '%s/' % context.website.base_url
    if context.take_screenshots:
        context.website.save_screenshot('homepage')
    assert_that(context.website.get_url(), equal_to(expected_url))


@then('I should be directed to the "www.consumerfinance.gov/{page_url}" URL')
def step(context, page_url):
    expected_url = '%s/%s' % (context.website.base_url, page_url)
    if context.take_screenshots:
        context.website.save_screenshot(page_url.replace('/', '_'))
    assert_that(context.website.get_url(), equal_to(expected_url))


@then('the page should load properly')
def step(context):
    assert_that(context.website.is_page_properly_loaded(),
                equal_to(True), 'Page did not properly load.')


@then(
    'I should see the page title as "{key_text} > Consumer Financial Protection Bureau"')
def step(context, key_text):
    expected_title = '%s > %s' % (key_text, agency_name)
    actual_title = context.website.get_title()
    assert_that(actual_title, equal_to(expected_title))


@then(
    'I should see the page title as "{key_text} - Consumer Financial Protection Bureau"')
def step(context, key_text):
    expected_title = '%s - %s' % (key_text, agency_name)
    actual_title = context.website.get_title()
    assert_that(actual_title, equal_to(expected_title))


@then('I should see the last breadcrumb as "{key_text}"')
def step(context, key_text):
    error_message = 'Text "%s" was not found on the page" % key_text'
    assert_that(context.website.is_text_last_in_breadcrumb(
        key_text), equal_to(True), error_message)


@then(u'I should find the text "{expected_text}" on the page')
def step(context, expected_text):
    error_message = 'Text "%s" was not found on the page" % key_text'
    assert_that(context.website.is_text_in_body(
        expected_text), equal_to(True), error_message)
