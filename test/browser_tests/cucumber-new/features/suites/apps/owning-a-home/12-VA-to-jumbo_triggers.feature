Feature: Test 12: VA to jumbo triggers, HP increase - Purpose: check for correct behavior when you trigger a VA HB loan successfully, then increase your house price, and you get kicked out to jumbo.
  As a first time visitor to the Rate Checker page
    I want to see FHA High Balance alerts
    So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance
Scenario Outline:
  When I select "<state_name>" as State
    And I select "VA" Loan Type
    And I enter "20" as Down Payment percent
    And I enter $"550,000" as House Price amount
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
Scenario Outline:
  When I select "<state_name>" as State
    And I select "VA" Loan Type
    And I enter "20" as Down Payment percent
    And I enter $"550,000" as House Price amount
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "VA high-balance" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "When you borrow between $424,100 and <VA_max_loan_amount> in your county, you may be eligible for a high-balance VA loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular VA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    But I should NOT see the County field highlighted

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

@high_balance
Scenario Outline:
  When I select "<state_name>" as State
    And I select "VA" Loan Type
    And I enter "20" as Down Payment percent
    And I enter $"550,000" as House Price amount
    And I select <county_name> County
    And I change the House Price amount to $"800,000"
  Then I should see the chart active with new data
    And I should see "Jumbo (non-conforming)" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "While VA loans do not have strict loan limits, most lenders are unlikely to make a VA loan more than <VA_max_loan_amount> in your county. Your only option may be a jumbo (non-conforming) loan."

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
