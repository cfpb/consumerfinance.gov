from behave import given, when, then
from hamcrest.core import assert_that, equal_to
from hamcrest.library.text.stringcontains import contains_string

# RELATIVE URLs
NEWSROOM = 'newsroom'
EVENTS = 'events'

@given(u'I navigate to the "{page_name}" page')
def step(context, page_name):
    if page_name == 'Newsroom':
        context.base.go(NEWSROOM)
    elif page_name == 'Events':
        context.base.go(EVENTS)
    else:
        raise Exception(page_name + ' is NOT a valid page')

@then(u'I should be directed to the internal "{relative_url}" URL')
def step(context, relative_url):
    actual_url = context.base.get_current_url()
    expected_url = context.utils.build_url(context.base_url, relative_url)
    assert_that(actual_url, equal_to(expected_url))

@when(u'I click on the "{link_name}" link')
def step(context, link_name):
    # Click the requested link
    context.navigation.click_link(link_name)

@then(u'I should see "{link_name}" displayed in the page title')
def step(context, link_name):
    # Verify that the page title matches the link we clicked
    page_title = context.base.get_page_title()
    assert_that(page_title, contains_string(link_name))