Feature: Verify the Retirement landing page works according to requirements
  As a first time visitor to the Retirement landing page
  I want to enter my age and income data on the landing page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the Retirement landing page

@smoke_testing @retirement @dob
Scenario Outline: Select month and day and year and income and retirement age
  Given I navigate to the Retirement Landing page
  When I enter month "<month>"
  And I enter day "<day>"
  And I enter year "<year>"
  And I enter income "<income>"
  And I click Get your estimates
  And I should see result "<retirement_age>" displayed in graph-container-text
  And I should find the text "full benefit claiming age" on the page
  When I move the slider on the graph to the left
  Then I should find the text "reduces your monthly benefit" on the page
  When I move the slider on the graph to the right
  Then I should find the text "increases your benefit" on the page

Examples:
| month | day | year | income | retirement_age   |
| 1     | 1   | 1954 | 50000  | 66               |
| 1     | 1   | 1955 | 50000  | 66               |
| 1     | 1   | 1956 | 50000  | 66 and 2 months  |
| 1     | 1   | 1957 | 50000  | 66 and 4 months  |
| 1     | 1   | 1958 | 50000  | 66 and 6 months  |
| 1     | 1   | 1959 | 50000  | 66 and 8 months  |
| 1     | 1   | 1960 | 50000  | 66 and 10 months |
| 1     | 1   | 1961 | 10000  | 67               |
| 2     | 2   | 1962 | 20000  | 67               |
| 3     | 3   | 1963 | 30000  | 67               |
| 4     | 4   | 1964 | 40000  | 67               |
| 5     | 5   | 1965 | 50000  | 67               |
| 6     | 6   | 1966 | 60000  | 67               |
| 7     | 7   | 1970 | 70000  | 67               |


@smoke_testing @retirement @lifestyle
Scenario Outline: Learn tips specific to your situation
   Given I navigate to the Retirement landing page
   And I enter birth and salary information
   When I respond to <question> by clicking <answer> in the tips blocks
Examples:
| question                                                                              | answer  |
| Are you married?                                                                      | Yes     |
| Are you married?                                                                      | No      |
| Are you married?                                                                      | Widowed |
| Do you plan to continue working in your 60s?                                          | Yes      |
| Do you plan to continue working in your 60s?                                          | No       |
| Do you plan to continue working in your 60s?                                          | Not Sure |
| Will your expenses decrease after you retire?                                         | Yes      |
| Will your expenses decrease after you retire?                                         | No       |
| Will your expenses decrease after you retire?                                         | Not Sure |
| Do you expect to have additional sources of retirement income beyond Social Security? | Yes      |
| Do you expect to have additional sources of retirement income beyond Social Security? | No       |
| Do you expect to have additional sources of retirement income beyond Social Security? | Not Sure |
| Do you expect to live a long life?                                                    | Yes      |
| Do you expect to live a long life?                                                    | No       |
| Do you expect to live a long life?                                                    | Not Sure |


@smoke_testing @retirement @age
Scenario Outline: Select the age you plan to start collecting your Social Security retirement benefits.
   Given I navigate to the Retirement landing page
   And I enter birth and salary information
   When I choose retirement age "<retirement_age>"
   Then I should see "<retirement_age>" in age-response-value
   And I answer whether or not the page was helpful
Examples:
| retirement_age |
| 62             |
| 63             |
| 64             |
| 65             |
| 66             |
| 67             |
| 68             |
| 69             |
| 70             |
