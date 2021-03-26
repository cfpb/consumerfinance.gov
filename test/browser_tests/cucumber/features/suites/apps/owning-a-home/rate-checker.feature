Feature: Verify the Rate Checker tool works according to requirements
  As a first time visitor to the Rate Checker page
  I want to utilize the Rate Checker tool
  So that I can make informed choices when shopping for a mortgage loan

Background:
  Given I navigate to the "Rate Checker" page

@rate_checker
Scenario Outline: Test selecting different states
  When I select "<state_name>" as State
  Then I should see the selected "<state_name>" above the Rate Checker chart
Examples:
| state_name |
| Nevada     |
| California |
| Virginia   |

@rate_checker
Scenario: Test all dropdown lists in the Rate Checker page
  When I select "Adjustable" Rate Structure
    And I select "7/1" ARM Type
    And I select "Fixed" Rate Structure
    And I select "15 Years" Loan Term
    And I select "FHA" Loan Type
