from behave import given, when, then
from hamcrest.core import assert_that, is_not, none
from hamcrest.library.number.ordering_comparison import greater_than, greater_than_or_equal_to
from hamcrest.library.text.stringcontains import contains_string
import requests
import json


@given(u'I select "{mortgage_house_price}" as Mortgage Insurance House Price')
def step(context, mortgage_house_price):
    context.query.mortgage_house_price = mortgage_house_price


@given(u'I omit the mortgage insurance "{mortgage_param_name}" field')
def step(context, mortgage_param_name):
    if(mortgage_param_name == "House Price"):
        context.query.mortgage_house_price = "missing"
    elif(mortgage_param_name == "Loan Amount"):
        context.query.mortgage_loan_amount = "missing"
    elif(mortgage_param_name == "Minimum Credit Score"):
        context.query.mortgage_minfico = "missing"
    elif(mortgage_param_name == "Maximum Credit Score"):
        context.query.mortgage_maxfico = "missing"
    elif(mortgage_param_name == "Rate Structure"):
        context.query.mortgage_rate_structure = "missing"
    elif(mortgage_param_name == "Loan Term"):
        context.query.mortgage_loan_term = "missing"
    elif(mortgage_param_name == "Loan Type"):
        context.query.mortgage_loan_type = "missing"
    elif(mortgage_param_name == "ARM Type"):
        context.query.mortgage_arm_type = "missing"
    elif(mortgage_param_name == "VA Status"):
        context.query.va_status = "missing"
    elif(mortgage_param_name == "First Time VA Loan Use"):
        context.query.va_first_use = "missing"


@given(u'I select "{mortgage_loan_amount}" as Mortgage Insurance Loan Amount')
def step(context, mortgage_loan_amount):
    context.query.mortgage_loan_amount = mortgage_loan_amount


@given(u'I select my mortgage insurance minimum credit score as "{mortgage_minfico}"')
def step(context, mortgage_minfico):
    context.query.mortgage_minfico = mortgage_minfico


@given(u'I select my mortgage insurance maximum credit score as "{mortgage_maxfico}"')
def step(context, mortgage_maxfico):
    context.query.mortgage_maxfico = mortgage_maxfico


@given(u'I select "{mortgage_rate_structure}" as Mortgage Insurance Rate Structure')
def step(context, mortgage_rate_structure):
    context.query.mortgage_rate_structure = mortgage_rate_structure


@given(u'I select "{mortgage_loan_term}" as Mortgage Insurance Loan Term')
def step(context, mortgage_loan_term):
    context.query.mortgage_loan_term = mortgage_loan_term


@given(u'I select "{mortgage_loan_type}" as Mortgage Insurance Loan Type')
def step(context, mortgage_loan_type):
    context.query.mortgage_loan_type = mortgage_loan_type


@given(u'I select "{mortgage_arm_type}" as Mortgage Insurance ARM Type')
def step(context, mortgage_arm_type):
    context.query.mortgage_arm_type = mortgage_arm_type


@given(u'I select "{va_status}" as VA Status')
def step(context, va_status):
    context.query.va_status = va_status


@given(u'I select "{va_first_use}" as First Time VA Loan Use')
def step(context, va_first_use):
    context.query.va_first_use = va_first_use


@when(u'I send the mortgage insurance request')
def step(context):
    query_string = context.query.build_mortgage()
    context.logger.debug("Query string is: %s" % query_string)

    context.response = requests.get(context.mortgage_url, params=query_string)
    context.logger.debug("URL is : %s" % context.response.url)


@then(u'the mortgage insurance response should include a data field')
def step(context):
    context.json_data = json.loads(context.response.text)
    context.logger.debug("What's in context json:%s" % context.json_data)
    context.logger.debug("JSON data is: %s" % context.json_data['data'])

    assert_that(len(context.json_data[u'data']), greater_than_or_equal_to(0))


@then(u'the mortgage insurance response should include a "{param_name}" field')
def step(context, param_name):
    context.json_data = json.loads(context.response.text)
    context.logger.debug("What's in context json:%s" % context.json_data)
    context.logger.debug("JSON data is: %s" % context.json_data[param_name])

    assert_that(len(context.json_data[param_name]), greater_than(0))


@then(u'the mortgage insurance response should state that required parameter "{param_name}" is required')
def step(context, param_name):
    context.json_data = json.loads(context.response.text)
    assert_that(context.json_data.get(param_name), is_not(none()))
    assert_that(context.json_data[param_name][0], contains_string('required'))


@then(u'the mortgage insurance response should include error stating "{html_text}"')
def step(context, html_text):
    context.json_data = json.loads(context.response.text)
    context.logger.debug("json_data html_text: %s" % context.json_data)
    assert_that(context.json_data.get('non_field_errors'), is_not(none()))
    assert_that(context.json_data['non_field_errors']
                [0], contains_string(html_text))


@then(u'the mortgage insurance response should NOT include "{html_text}"')
def step(context, html_text):
    assert_that(context.response.text, is_not(contains_string(html_text)))
