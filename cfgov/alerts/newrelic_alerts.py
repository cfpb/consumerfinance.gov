import datetime
import re

import requests


class NewRelicAlertViolations:

    newrelic_url = 'https://api.newrelic.com/v2/'

    def __init__(self, newrelic_token, policy_filter, account_number,
                 known_violations=[]):
        self.newrelic_token = newrelic_token
        self.policy_filter_re = re.compile(policy_filter)
        self.account_number = account_number
        self.known_violations = known_violations

    def get_current_violations(self):
        """ Check for all violations currently open in New Relic """
        headers = {'X-Api-Key': self.newrelic_token}
        violations_url = (self.newrelic_url +
                          'alerts_violations.json?only_open=true')
        r = requests.get(violations_url, headers=headers)
        r.raise_for_status()
        response_json = r.json()

        # Filter on the policy name
        violations = [v for v in response_json['violations']
                      if self.policy_filter_re.search(v['policy_name'])]

        return violations

    def get_new_violations(self):
        """ Determine which current violations are new. Non-new violations
        are expected to be in known_violations. Any violations returned by
        this method are automatically added to known_violations. """
        violations = []
        for violation in self.get_current_violations():
            if violation['id'] in self.known_violations:
                continue

            self.known_violations.append(violation['id'])
            violations.append(violation)

        return violations

    def get_new_violation_messages(self):
        violations = self.get_new_violations()
        formatted_violations = [self.format_violation(v)
                                for v in violations]
        return formatted_violations

    def format_violation(self, violation):
        """ Format the given violation dictionary into an SQS message
        dictionary """
        opened_timestamp = violation['opened_at'] / 1000.0
        opened = datetime.datetime.fromtimestamp(opened_timestamp)
        opened_str = opened.strftime('%a, %b %d %Y, at %I:%M %p %z')
        title = '{condition_name}, {entity_name}'.format(
            condition_name=violation['condition_name'],
            entity_name=violation['entity']['name']
        )
        incidents_link = (
            'https://alerts.newrelic.com/accounts/'
            '{account_number}/incidents'
        ).format(
            account_number=self.account_number
        )
        body = (
            'New Relic {product}, {name}, {label} '
            '({priority}, opened {opened}, violation id {id}).'
            'View incidents: {link}'
        ).format(
            product=violation['entity']['product'],
            label=violation['label'],
            name=violation['entity']['name'],
            id=violation['id'],
            priority=violation['priority'],
            opened=opened_str,
            link=incidents_link
        )
        message_body = '{title} - {body}'.format(title=title, body=body)
        return message_body
