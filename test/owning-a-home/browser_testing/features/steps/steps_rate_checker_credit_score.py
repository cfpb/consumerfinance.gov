from behave import then, when
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.number.ordering_comparison import greater_than, less_than
from hamcrest.library.text.stringcontains import contains_string
from hamcrest.core.core.isnot import is_not


# DEFAULT VALUES
DEFAULT_CREDIT_SCORE = 700  # the default range is 700 - 720
RANGE_ALERT_TEXT = ("Many lenders do not accept borrowers "
                    "with credit scores less than 620")


# CREDIT SCORE RANGE
@when(u'I move the credit score slider to the "{slider_direction}" range')
@when(u'I move the credit score slider to the "{slider_direction}"')
def step(context, slider_direction):
    context.rate_checker.set_credit_score_range(slider_direction)


@then(u'I should see the Credit Score Range displayed as "{score}"')
def step(context, score):
    actual_text = context.rate_checker.get_credit_score_range()
    assert_that(actual_text, equal_to(score))


@then(u'I should see the credit score range "{range_operation}"')
def step(context, range_operation):
    # get the range text from below the slider handle
    range_text = context.rate_checker.get_credit_score_range()
    currentRange = int(range_text[:3])

    if (range_operation == "increase"):
        assert_that(currentRange, greater_than(DEFAULT_CREDIT_SCORE))
    elif (range_operation == "decrease"):
        assert_that(currentRange, less_than(DEFAULT_CREDIT_SCORE))


# ALERTS
@then(u'I should see an alert for borowers with less than 620 score')
def step(context):
    actual_text = context.rate_checker.get_range_alert_text()
    assert_that(actual_text, contains_string(RANGE_ALERT_TEXT))


@then(u'I should NOT see an alert for borowers with less than 620 score')
def step(context):
    actual_text = context.rate_checker.get_range_alert_text()
    assert_that(actual_text, equal_to(False))


@then(u'I should see the credit score slider handle turns "{handle_color}"')
def step(context, handle_color):
    actual_text = context.rate_checker.get_warning_button_class()
    # If the element's class name includes 'warning'
    # Then the button has turned red
    if(handle_color == 'red'):
        assert_that(actual_text, contains_string("warning"))
    # If the element's class name DOES NOT include 'warning'
    # Then the button has turned green
    elif(handle_color == 'green'):
        assert_that(actual_text, is_not(contains_string("warning")))
