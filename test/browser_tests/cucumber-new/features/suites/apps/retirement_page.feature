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
  And I click Get your estimates
  And I choose retirement age "<retirement_age>"
  Then I should see "<retirement_age>" in age_selector_response
  And I should see result "<expected_result>" displayed in graph-container-text

Examples:
| month | day | year | income | expected_result  | retirement_age |
| 1     | 1   | 1954 | 50000  | 66               | 65             |
| 1     | 1   | 1955 | 50000  | 66               | 64             |
| 1     | 1   | 1956 | 50000  | 66 and 2 months  | 63             |
| 1     | 1   | 1957 | 50000  | 66 and 4 months  | 62             |
| 1     | 1   | 1958 | 50000  | 66 and 6 months  | 62             |
| 1     | 1   | 1959 | 50000  | 66 and 8 months  | 62             |
| 1     | 1   | 1960 | 50000  | 66 and 10 months | 62             |
| 1     | 1   | 1961 | 10000  | 67               | 67             |
| 2     | 2   | 1962 | 20000  | 67               | 67             |
| 3     | 3   | 1963 | 30000  | 67               | 67             |
| 4     | 4   | 1964 | 40000  | 67               | 67             |
| 5     | 5   | 1965 | 50000  | 67               | 62             |
| 6     | 6   | 1966 | 60000  | 67               | 67             |
| 7     | 7   | 1970 | 70000  | 67               | 70             |
