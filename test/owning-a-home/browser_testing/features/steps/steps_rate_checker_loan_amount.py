from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from decorators import handle_error


# HOUSE PRICE
@given(u'I enter $"{house_price}" as House Price amount')
@when(u'I enter $"{house_price}" as House Price amount')
@when(u'I change the House Price amount to $"{house_price}"')
def step(context, house_price):
    # Wait for the chart to load
    assert_that(context.rate_checker.is_chart_loaded(),
                equal_to("Chart is loaded"))
    # Set House Price
    context.rate_checker.set_house_price(house_price)
    # Wait for the chart to load
    # assert_that(context.rate_checker.is_chart_loaded(), equal_to("Chart is loaded"))


@then(u'I should see $"{house_price}" as the House price')
def step(context, house_price):
    current_Amount = context.rate_checker.get_house_price()
    assert_that(current_Amount, equal_to(house_price))


# DOWN PAYMENT PERCENT
@given(u'I enter "{down_payment}" as Down Payment percent')
@when(u'I enter "{down_payment}" as Down Payment percent')
@when(u'I change the Down Payment percent to "{down_payment}"')
def step(context, down_payment):
    context.rate_checker.set_down_payment_percent(down_payment)


@then(u'I should see "{dp_percent}" as Down Payment percent')
def step(context, dp_percent):
    current_Percent = context.rate_checker.get_down_payment_percent()
    assert_that(current_Percent, equal_to(dp_percent))


# DOWN PAYMENT AMOUNT
@when(u'I enter $"{dp_amount}" as Down Payment amount')
@when(u'I change the Down Payment amount to $"{dp_amount}"')
def step(context, dp_amount):
    context.rate_checker.set_down_payment_amount(dp_amount)


@then(u'I should see $"{dp_amount}" as Down Payment amount')
def step(context, dp_amount):
    current_Amount = context.rate_checker.get_down_payment_amount()
    assert_that(current_Amount, equal_to(dp_amount))


@then(u'I should see a DP alert "{alert_text}"')
def step(context, alert_text):
    actual_text = context.rate_checker.get_dp_alert_text(alert_text)
    assert_that(actual_text, equal_to(alert_text))

# LOAN AMOUNT


@then(u'I should see "{expected_loan_amount}" as Loan Amount')
def step(context, expected_loan_amount):
    actual_loan_amount = context.rate_checker.get_loan_amount()
    assert_that(actual_loan_amount, equal_to(expected_loan_amount))


# COUNTY
@given(u'I select {county_name} County')
@when(u'I select {county_name} County')
@handle_error
def step(context, county_name):
    # context.base.sleep(2)
    context.rate_checker.set_county(county_name)


@then(u'I should NOT see the County selection')
def step(context):
    county = context.rate_checker.is_county_visible()
    assert_that(county, equal_to(False))


@then(u'I should see a County alert "{alert_text}"')
@handle_error
def step(context, alert_text):
    actual_text = context.rate_checker.get_county_alert_text(alert_text)
    assert_that(actual_text, equal_to(True))


@then(u'I should NOT see a County alert "{alert_text}"')
def step(context, alert_text):
    actual_text = context.rate_checker.get_county_alert_text(alert_text)
    assert_that(actual_text, equal_to(False))


@then(u'I should see the County field highlighted')
def step(context):
    actual_state = context.rate_checker.is_county_highlighted()
    assert_that(actual_state, equal_to(True))


@then(u'I should NOT see the County field highlighted')
def step(context):
    actual_state = context.rate_checker.is_county_highlighted()
    assert_that(actual_state, equal_to(False))
