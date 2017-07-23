from behave import given, when, then
from hamcrest.core import assert_that, is_not, none
from hamcrest.library.number.ordering_comparison import greater_than
from hamcrest.library.text.stringcontains import contains_string
import requests
import json


@given(u'I select "{house_price}" as House Price')
def step(context, house_price):
    context.query.house_price = house_price


@given(u'I omit the "{param_name}" field')
def step(context, param_name):
    if(param_name == "House Price"):
        context.query.house_price = "missing"
    elif(param_name == "Loan Amount"):
        context.query.loan_amount = "missing"
    elif(param_name == "Minimum Credit Score"):
        context.query.minfico = "missing"
    elif(param_name == "Maximum Credit Score"):
        context.query.maxfico = "missing"
    elif(param_name == "State"):
        context.query.state = "missing"
    elif(param_name == "Rate Structure"):
        context.query.rate_structure = "missing"
    elif(param_name == "Loan Term"):
        context.query.loan_term = "missing"
    elif(param_name == "Loan Type"):
        context.query.loan_type = "missing"
    elif(param_name == "ARM Type"):
        context.query.arm_type = "missing"


@given(u'I select "{loan_amount}" as Loan Amount')
def step(context, loan_amount):
    context.query.loan_amount = loan_amount


@given(u'I select my minimum credit score as "{minfico}"')
def step(context, minfico):
    context.query.minfico = minfico


@given(u'I select my maximum credit score as "{maxfico}"')
def step(context, maxfico):
    context.query.maxfico = maxfico


@given(u'I select "{state}" as State')
def step(context, state):
    context.query.state = state


@given(u'I select "{rate_structure}" as Rate Structure')
def step(context, rate_structure):
    context.query.rate_structure = rate_structure


@given(u'I select "{loan_term}" as Loan Term')
def step(context, loan_term):
    context.query.loan_term = loan_term


@given(u'I select "{loan_type}" as Loan Type')
def step(context, loan_type):
    context.query.loan_type = loan_type


@given(u'I select "{arm_type}" as ARM Type')
def step(context, arm_type):
    context.query.arm_type = arm_type


@when(u'I send the request')
def step(context):
    query_string = context.query.build()
    context.logger.debug("Query string is: %s" % query_string)

    context.response = requests.get(context.base_url, params=query_string)
    context.logger.debug("URL is : %s" % context.response.url)


@then(u'the response should include a timestamp field')
def step(context):
    context.json_data = json.loads(context.response.text)
    context.logger.debug("timestamp is: %s" % context.json_data['timestamp'])
    assert_that(len(context.json_data[u'timestamp']), greater_than(0))


@then(u'the response should include a data field')
def step(context):
    context.json_data = json.loads(context.response.text)
    context.logger.debug("JSON data is: %s" % context.json_data['data'])

    assert_that(len(context.json_data[u'data']), greater_than(0))


@then(u'the response should state that required parameter "{param_name}" is required')
def step(context, param_name):
    context.json_data = json.loads(context.response.text)
    assert_that(context.json_data.get(param_name), is_not(none()))
    assert_that(context.json_data[param_name][0], contains_string('required'))


@then(u'the response should NOT include "{html_text}"')
def step(context, html_text):
    assert_that(context.response.text, is_not(contains_string(html_text)))
