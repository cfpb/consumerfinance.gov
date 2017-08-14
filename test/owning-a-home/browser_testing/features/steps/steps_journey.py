# coding: utf-8
from behave import then
from hamcrest.core import assert_that, equal_to


@then(u'I see page loaded')
def navbar_is_loaded(context):
    assert_that(context.journey.is_navbar_found(),
                equal_to(True), 'Navbar found')
