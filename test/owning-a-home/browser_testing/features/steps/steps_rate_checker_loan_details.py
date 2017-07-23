from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to


# RATE STRUCTURE
@when(u'I select "{rate_selection}" Rate Structure')
def step(context, rate_selection):
    context.rate_checker.set_rate_structure(rate_selection)


@then(u'I should see "{loan_structure}" as the selected Rate Structure')
def step(context, loan_structure):
    current_Selection = context.rate_checker.get_rate_structure()
    assert_that(current_Selection, equal_to(loan_structure))


# LOAN TERM
@when(u'I select "{number_of_years}" Loan Term')
def step(context, number_of_years):
    context.rate_checker.set_loan_term(number_of_years)


@then(u'I should see "{number_of_years}" as the selected Loan Term')
def step(context, number_of_years):
    current_Selection = context.rate_checker.get_loan_term()
    assert_that(current_Selection, equal_to(number_of_years))


@then(u'Loan term option "{loan_term}" should be "{expected_state}"')
def step(context, loan_term, expected_state):
    actual_state = context.rate_checker.is_loan_term_option_enabled(loan_term)
    assert_that(actual_state, equal_to(expected_state))


# LOAN TYPE
@given(u'I select "{loan_type}" Loan Type')
@when(u'I change to "{loan_type}" Loan Type')
@when(u'I select "{loan_type}" Loan Type')
def step(context, loan_type):
    context.rate_checker.set_loan_type(loan_type)


@then(u'I should see "{loan_type}" as the selected Loan Type')
def step(context, loan_type):
    current_Selection = context.rate_checker.get_selected_loan_type()
    assert_that(current_Selection, equal_to(loan_type))


@then(u'I should see the Loan Type field highlighted')
def step(context):
    actual_state = context.rate_checker.is_loan_type_highlighted()
    assert_that(actual_state, equal_to(True))


@then(u'I should NOT see the Loan Type field highlighted')
def step(context):
    actual_state = context.rate_checker.is_loan_type_highlighted()
    assert_that(actual_state, equal_to(False))


@then(u'I should see an HB alert "{alert_text}"')
def step(context, alert_text):
    actual_text = context.rate_checker.get_hb_alert_text(alert_text)
    assert_that(actual_text, equal_to(alert_text))


@then(u'I should NOT see an HB alert "{alert_text}"')
def step(context, alert_text):
    actual_text = context.rate_checker.is_hb_alert_hidden(alert_text)
    assert_that(actual_text, equal_to(alert_text))


@then(u'Loan type option "{loan_type}" should be "{expected_state}"')
def step(context, loan_type, expected_state):
    actual_state = context.rate_checker.is_loan_type_option_enabled(loan_type)
    assert_that(actual_state, equal_to(expected_state))


# ARM TYPE
@when(u'I select "{arm_type}" ARM Type')
def step(context, arm_type):
    context.rate_checker.set_arm_type(arm_type)


@then(u'I should see "{arm_type}" as the selected ARM Type')
def step(context, arm_type):
    current_Selection = context.rate_checker.get_arm_type()
    assert_that(current_Selection, equal_to(arm_type))


@then(u'I should NOT see the ARM Type selection')
def step(context):
    arm_type_selection = context.rate_checker.is_arm_type_visible()
    assert_that(arm_type_selection, equal_to(False))


@then(u'I should see the ARM Type field highlighted')
def step(context):
    actual_state = context.rate_checker.is_arm_type_highlighted()
    assert_that(actual_state, equal_to(True))


@then(u'I should NOT see the ARM Type field highlighted')
def step(context):
    actual_state = context.rate_checker.is_arm_type_highlighted()
    assert_that(actual_state, equal_to(False))


# INTEREST COST LABEL
@then(u'I should see primary Interest costs over the first "{loan_years}" years')
@then(u'I should see primary Interest costs over "{loan_years}" years')
def step(context, loan_years):
    actual_text = context.rate_checker.get_primary_interest_rate(loan_years)

    assert_that(actual_text, equal_to(loan_years))


@then(u'I should see Interest costs over the first "{total_years}" years')
@then(u'I should see Interest costs over "{total_years}" years')
def step(context, total_years):
    actual_text = context.rate_checker.get_secondary_interest_rate(total_years)

    assert_that(actual_text, equal_to(total_years))
