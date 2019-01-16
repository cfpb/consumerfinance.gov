Feature: Feedback form
  As a user of cf.gov
  I should be able to use the feedback form
  to submit feedback

  Scenario: Submit form without feedback
    Given I goto URL "/feedback"
    When I click the feedback form submit button
    Then the notification element should be displayed
    And the notification should report an error
    And the feedback form should be present

  Scenario: Submit form with radio selection
    Given I goto URL "/feedback"
    When I select a feedback radio button
    And I click the feedback form submit button
    Then the notification element should be displayed
    And the notification should report success
    And the feedback form should no longer be present

  Scenario: Submit form with comment
    Given I goto URL "/feedback"
    When I enter a comment
    And I click the feedback form submit button
    Then the notification element should be displayed
    And the notification should report success
    And the feedback form should no longer be present