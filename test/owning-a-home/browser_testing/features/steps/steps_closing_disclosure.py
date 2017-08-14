# coding: utf-8
from behave import then, when
from hamcrest.core import assert_that, equal_to


@then(u'I should see "{tab_name}" tab')
def tab_is_found(context, tab_name):
    assert_that(context.closing_disclosure.tab_is_found(tab_name), equal_to(True),
                'Tab %s found' % tab_name)


@then(u'Content image is loaded')
def content_image_is_loaded(context):
    assert_that(context.closing_disclosure.content_image_is_loaded(), equal_to(True),
                'Content image is loaded')


@when(u'I resize window image "{css_selector}" size changes too')
def resizing_window_changes_image_size(context, css_selector):
    original_size = context.closing_disclosure._element_size(css_selector)
    context.closing_disclosure.resize_to_mobile_size()
    new_size = context.closing_disclosure._element_size(css_selector)
    assert_that(original_size, not equal_to(new_size),
                'Sizes are not the same original: %s, new: %s' % (original_size, new_size))


@then(u'Expandable explainers for "{tab_name}" are loaded')
def expandable_explainers_are_loaded(context, tab_name):
    result = context.closing_disclosure.expandable_explainers_are_loaded(
        tab_name)
    assert_that(result, not equal_to(0),
                'Expandable explainers on %s tab are loaded ok' % tab_name)


@then(u'Expandable explainers for tab other than "{tab_name}" are invisible')
def other_expandable_explainers_are_invisible(context, tab_name):
    other_tab = 'definitions' if tab_name == 'Checklist' else 'checklist'
    result = context.closing_disclosure.expandable_explainers_are_loaded(
        other_tab)
    assert_that(result, equal_to(0),
                'Other expandable explainers for %s are invisible' % other_tab)


@when(u'I click the tab "{tab_name}"')
def click_tab(context, tab_name):
    context.closing_disclosure._click_tab(tab_name)


@when(u'I hover over an overlay the corresponding explainer has class hover-has-attention')
def hover_an_overlay(context):
    result = context.closing_disclosure.hover_an_overlay()
    assert_that(result, equal_to(
        0), 'All overlays to explainers connections work')


@when(u'I click an overlay the corresponding explainer has class has-attention')
def hover_an_overlay(context):
    result = context.closing_disclosure.click_an_overlay()
    assert_that(result, equal_to(
        0), 'All overlays to explainers connections work')


@when(u'I click on page "{page_num}"')
def click_page(context, page_num):
    context.closing_disclosure.click_page(page_num)


@then(u'page "{page_num}" is displayed')
def page_is_current(context, page_num):
    current_page = context.closing_disclosure.current_page()

    assert_that(current_page, equal_to(page_num),
                'Page %s is current page' % current_page)


@when(u'I click the next button in page "{current_num}"')
def click_next_page(context, current_num):
    context.closing_disclosure.click_next_page(current_num)


@when(u'I click the previous button in page "{current_num}"')
def click_prev_page(context, current_num):
    context.closing_disclosure.click_prev_page(current_num)


@when(u'I click page "{current_num}" in Form Explainer')
def click_page_number(context, current_num):
    context.closing_disclosure.click_page(current_num)
