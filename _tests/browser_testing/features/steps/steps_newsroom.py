from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.text.stringcontains import contains_string


# Category checkbox
@when(u'I click the checkbox for "{category_name}"')
def step(context, category_name):
    context.click_category_checkbox(category_name)


# Filter button
@when(u'I click Apply filters')
def step(context):
    context.click_apply_filters()

@when(u'I click Clear filters')
def step(context):
    context.click_clear_filters()

@given(u'I click the Filter posts button')
def step(context):
    context.click_filter_posts_button()


# Filter dropdown
@when(u'I set a date filter of "{from_month}", "{from_year}" to "{to_month}", "{to_year}"')
def step(context, from_month, from_year, to_month, to_year):
    context.set_date_filter(from_month, from_year, to_month, to_year)


# Author and topic searches
@when(u'I enter "{topic_search}" into the topic search box')
def step(context, topic_search):
    context.enter_text_into_search_filter('topic', topic_search)

@when(u'I click the "{topic_name}" option in the results')
def step(context, topic_name):
    context.select_search_filter('topic', topic_name)

@when(u'I enter "{author_search}" into the author search box')
def step(context, author_search):
    context.enter_text_into_search_filter('author', author_search)

@when(u'I click the "{author_name}" option in the results')
def step(context, author_name):
    context.select_search_filter('author', author_name)


# Results
@then(u'I should see "{results_number}" results')
def step(context, results_number):
    actual_results = context.get_results_number()
    assert_that(actual_results, equal_to(results_number))

@then(u'I should see "{from_date}" as the listed From Date')
def step(context, from_date):
    filter_text = context.get_filter_used()
    assert_that(filter_text, contains_string(from_date))

@then(u'I should see "{to_date}" as the listed To Date')
def step(context, to_date):
    filter_text = context.get_filter_used()
    assert_that(filter_text, contains_string(to_date))

@then(u'I should see "{author_name}" as the listed filter')
def step(context, author_name):
    filter_text = context.get_filter_used()
    assert_that(filter_text, contains_string(author_name))

@then(u'I should see "{topic_name}" as the listed filter')
def step(context, topic_name):
    filter_text = context.get_filter_used()
    assert_that(filter_text, contains_string(topic_name))

@then(u'I should see 0 filters chosen')
def step(context):
    filters_selected = context.are_filters_selected()
    assert_that(filters_selected, equal_to(False))

@then(u'I should see the checkbox next to "{category_name}" unchecked')
def step(context, category_name):
    checked = is_category_checked(category_name)
    assert_that(checked, equal_to(False))

@then(u'I should not see pagination displayed')
def step(context):
    pagination_displayed = context.is_pagination_displayed()
    assert_that(pagination_displayed, equal_to(False))


# Pagination
@when(u'I click the Next button')
def step(context):
    context.click_pagination_button('next')

@when(u'I click the Previous button')
def step(context):
    context.click_pagination_button('previous')

@when(u'I click the "{page_number}" button')
def step(context, page_number):
    context.click_pagination_button(page_number)

@then(u'I should see a current page value of "{current_page}"')
def step(context, current_page):
    page_num_displayed = context.get_current_page_number()
    assert_that(page_num_displayed, equal_to(current_page))
