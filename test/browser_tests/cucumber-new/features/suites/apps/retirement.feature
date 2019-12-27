Feature: Verify the Retirement landing page works according to requirements
  As a first time visitor to the Retirement landing page
  I want to enter my age and income data on the landing page
  So that I can find the information I'm looking for

@smoke_testing @retirement @dob
Scenario Outline: Select month and day and year and income and retirement age
  Given I visit the consumerfinance consumer-tools/retirement/before-you-claim URL
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
  Given I visit the consumerfinance consumer-tools/retirement/before-you-claim URL
  And I enter birth and salary information
  When I respond to <question> by clicking <answer> in the tips blocks
  Then I should find the text "<response_text>" on the page
Examples:
| question                                                                              | answer  | response_text |
| Are you married?                                                                      | Yes     | You can protect the financial security of your surviving spouse. |
| Are you married?                                                                      | No      | Claiming at your full retirement age or later permanently increases your benefit. |
| Are you married?                                                                      | Widowed | Your claiming age matters for your own retirement benefits and your survivor's benefits. |
| Do you plan to continue working in your 60s?                                          | Yes      | Working in your 60s will help you maximize your income and savings. |
| Do you plan to continue working in your 60s?                                          | No       | You can maximize your benefits even if you work fewer hours or stop working. |
| Do you plan to continue working in your 60s?                                          | Not Sure | Consider working in your 60s for an extra boost to your income and savings. |
| Will your expenses decrease after you retire?                                         | Yes      | Retirement could be more expensive than you expect. |
| Will your expenses decrease after you retire?                                         | No       | Maintain your lifestyle by planning ahead. |
| Will your expenses decrease after you retire?                                         | Not Sure | Many people find retirement is more expensive than expected. |
| Do you expect to have additional sources of retirement income beyond Social Security? | Yes      | Continue saving in the coming years. |
| Do you expect to have additional sources of retirement income beyond Social Security? | No       | It's a perfect time to start saving. |
| Do you expect to have additional sources of retirement income beyond Social Security? | Not Sure | There are many ways to plan for a secure retirement outside of Social Security. |
| Do you expect to live a long life?                                                    | Yes      | Many people live longer than they expect. |
| Do you expect to live a long life?                                                    | No       | Claiming at your full benefit age could still make sense for you. |
| Do you expect to live a long life?                                                    | Not Sure | There's a good chance that you'll live into your 80s and beyond. |


@smoke_testing @retirement @age
Scenario Outline: Select the age you plan to start collecting your Social Security retirement benefits.
  Given I visit the consumerfinance consumer-tools/retirement/before-you-claim URL
  And I enter birth and salary information
  When I choose retirement age "<retirement_age>"
  Then I should see "<retirement_age>" in age-response-value
  And I should find the text "<retirement_text>" on the page
  And I answer whether or not the page was helpful
  Then I should find the text "Thank you for your feedback!" on the page
Examples:
| retirement_age | retirement_text                                                                                |
| 62             | You’ve chosen age 62, which is earlier than your Social Security full retirement claiming age. |
| 63             | You’ve chosen age 63, which is earlier than your Social Security full retirement claiming age. |
| 64             | You’ve chosen age 64, which is earlier than your Social Security full retirement claiming age. |
| 65             | You’ve chosen age 65, which is earlier than your Social Security full retirement claiming age. |
| 66             | You’ve chosen age 66, which is earlier than your Social Security full retirement claiming age. |
| 67             | You’ve chosen age 67, which is your Social Security full retirement claiming age.              |
| 68             | You’ve chosen age 68, which is later than your Social Security full retirement claiming age.   |
| 69             | You’ve chosen age 69, which is later than your Social Security full retirement claiming age.   |
| 70             | You’ve chosen age 70, which is your maximum Social Security benefit claiming age.              |
