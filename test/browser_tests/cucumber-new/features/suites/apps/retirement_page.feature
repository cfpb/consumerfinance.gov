Feature: Verify the Retirement landing page works according to requirements
  As a first time visitor to the Retirement landing page
  I want to enter my age and income data on the landing page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the Retirement landing page

@smoke_testing @retirement
Scenario Outline: Select month and day and year and income and retirement age
  Given I navigate to the Retirement Landing page
  When I enter month "<month>"
  And I enter day "<day>"
  And I enter year "<year>"
  And I enter income "<income>"
  And I click get estimate
  And I choose retirement age "<retirement_age>"
  Then I should see "<retirement_age>" in age_selector_response
  And I should see result "<expected_result>" displayed in graph-container-text

Examples:
| month | day | year | income | expected_result | retirement_age |
| 7     | 7   | 1970 | 70000  | 67              | 70             |
| 6     | 6   | 1966 | 60000  | 67              | 67             |
| 5     | 5   | 1965 | 50000  | 67              | 62             |
