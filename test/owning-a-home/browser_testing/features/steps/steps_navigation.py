# coding: utf-8
from behave import given, when, then
from hamcrest.core import assert_that, equal_to
from hamcrest.library.text.stringcontains import contains_string
from decorators import handle_error


# XPATH LOCATORS

# RELATIVE URL'S
HOME = 'index.html'
LO = 'loan-options'
CONV = 'loan-options/conventional-loans'
ER = 'explore-rates'
FHA = 'loan-options/FHA-loans'
SPECIAL = 'loan-options/special-loan-programs'
# Journey links
KP = 'process'
PP = 'process/prepare'
PE = 'process/explore'
PC = 'process/compare'
PF = 'process/close'
PS = 'process/sources'
# FE
CD = 'closing-disclosure'
LE = 'loan-estimate'
# Form Resources
MC = 'mortgage-closing'
ME = 'mortgage-estimate'


@given(u'I navigate to the "{page_name}" page')
@handle_error
def step(context, page_name):
    if (page_name == 'Owning a Home'):
        context.base.go(HOME)
    elif (page_name == 'Loan Options'):
        context.base.go(LO)
    elif (page_name == 'Rate Checker'):
        context.base.go(ER)
        # Wait for the chart to load
        context.base.sleep(2)
        assert_that(context.rate_checker.is_chart_loaded(),
                    equal_to("Chart is loaded"))
    elif (page_name == 'Conventional Loan'):
        context.base.go(CONV)
    elif (page_name == 'FHA Loan'):
        context.base.go(FHA)
    elif (page_name == 'Special Loan Programs'):
        context.base.go(SPECIAL)
    elif (page_name == 'Know the Process'):
        context.base.go(KP)
    elif (page_name == 'Prepare to Shop'):
        context.base.go(PP)
    elif (page_name == 'Explore Loan Options'):
        context.base.go(PE)
    elif (page_name == 'Compare Loan Options'):
        context.base.go(PC)
    elif (page_name == 'Get Ready to Close'):
        context.base.go(PF)
    elif (page_name == 'Sources'):
        context.base.go(PS)
    elif (page_name == 'Closing Disclosure'):
        context.base.go(CD)
    elif (page_name == 'Loan Estimate'):
        context.base.go(LE)
    elif (page_name == 'Mortgage Closing'):
        context.base.go(MC)
    elif (page_name == 'Mortgage Estimate'):
        context.base.go(ME)
    else:
        raise Exception(page_name + ' is NOT a valid page')


@given(u'I navigate to the OAH Landing page')
@handle_error
def step(context):
    context.base.go()


@when(u'I click on the "{link_name}" link')
@handle_error
def step(context, link_name):
    # Click the requested tab
    context.navigation.click_link(link_name)


@when(u'I click on the link with id "{link_id}"')
@handle_error
def step(context, link_id):
    # Click the requested tab
    context.navigation.click_link_with_id(link_id)


@then(u'I should see "{link_name}" displayed in the page title')
@handle_error
def step(context, link_name):
    # Verify that the page title matches the link we clicked
    page_title = context.base.get_page_title()
    assert_that(page_title, contains_string(link_name))


@then(u'I should see the page scroll to the "{page_anchor}" section')
@handle_error
def step(context, page_anchor):
    current_url = context.base.get_current_url()
    assert_that(current_url, contains_string(page_anchor))


@then(u'I should be directed to the internal "{relative_url}" URL')
@handle_error
def step(context, relative_url):
    actual_url = context.base.get_current_url()
    expected_url = context.utils.build_url(context.base_url, relative_url)
    assert_that(actual_url, equal_to(expected_url))


@then(u'I should be directed to the external "{full_url}" URL')
@handle_error
def step(context, full_url):
    actual_url = context.base.get_current_url()
    assert_that(actual_url, contains_string(full_url))


@then(u'I should be directed to the OAH Landing page')
@handle_error
def step(context):
    actual_url = context.base.get_current_url()
    expected_url = context.utils.build_url(context.base_url, '/')
    assert_that(actual_url, equal_to(expected_url))


@then(u'I should see the "{relative_url}" URL with page title {page_title} open in a new tab')
@handle_error
def step(context, relative_url, page_title):
    title = context.base.switch_to_new_tab(relative_url)
    assert_that(title, contains_string(page_title))


@then(u'Links are working without 404 errors')
def links_working_without_404s(context):
    assert_that(context.navigation.check_links_for_404s(context.base_url),
                equal_to([]),
                'Broken links on <%s>' % context.base.get_current_url())
