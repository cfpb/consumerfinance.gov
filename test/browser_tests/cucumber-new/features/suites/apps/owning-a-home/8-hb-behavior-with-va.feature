Feature: Test 8: Basic HB behavior with VA - Purpose: check for correct behavior when you trigger a VA HB loan.
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I select "VA" Loan Type
    And I enter $"500,000" as House Price amount
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular VA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name     |
| California     |
| Colorado       |
| Florida        |
| Idaho          |
| Maryland       |
| North Carolina |
| Virginia       |
| Washington     |

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I select "VA" Loan Type
    And I enter $"500,000" as House Price amount
    #And I wait "10" seconds and do nothing
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular VA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see "VA high-balance" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "When you borrow between $424,100 and <VA_max_loan_amount> in your county, you may be eligible for a high-balance VA loan."

Examples:
| state_name     | county_name         | VA_max_loan_amount |
| California     | Mono County         | $529,000           |
| Colorado       | San Miguel County   | $625,500           |
| Florida        | Monroe County       | $529,000           |
| Idaho          | Blaine County       | $625,500           |
| Maryland       | Anne Arundel County | $517,500           |
| North Carolina | Gates County        | $458,850           |
| Virginia       | Norfolk city        | $458,850           |
| Washington     | Snohomish County    | $540,500           |
