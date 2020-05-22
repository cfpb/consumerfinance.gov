Feature: Test 6: Changing loan types - Purpose: check for correct behavior when you change the loan type in the $275,665 - $424,100 range in counties with FHA-HB available.
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name   |
| Georgia      |
| Illinois     |
| Maryland     |
| New Jersey   |
| Oregon       |
| Pennsylvania |
| Virginia     |
| Wisconsin    |
| Georgia      |
| Illinois     |
| Maryland     |
| New Jersey   |
| Oregon       |
| Pennsylvania |
| Virginia     |
| Wisconsin    |

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
   And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "FHA high-balance" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "When you borrow between $275,665 and <FHA_max_loan_amount> in your county, you are eligible for a high-balance FHA loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    But I should NOT see the County field highlighted

Examples:
| state_name   | county_name       | FHA_max_loan_amount | new_loan_type |
| Georgia      | Cobb County       | $342,700            | VA            |
| Illinois     | Kane County       | $365,700            | VA            |
| Maryland     | Baltimore city    | $517,500            | VA            |
| New Jersey   | Monmouth County   | $625,500            | VA            |
| Oregon       | Hood River County | $371,450            | VA            |
| Pennsylvania | Lehigh County     | $372,600            | VA            |
| Virginia     | Amelia County     | $535,900            | VA            |
| Wisconsin    | St. Croix County  | $326,600            | VA            |
| Georgia      | Cobb County       | $342,700            | Conventional  |
| Illinois     | Kane County       | $365,700            | Conventional  |
| Maryland     | Baltimore city    | $517,500            | Conventional  |
| New Jersey   | Monmouth County   | $625,500            | Conventional  |
| Oregon       | Hood River County | $371,450            | Conventional  |
| Pennsylvania | Lehigh County     | $372,600            | Conventional  |
| Virginia     | Amelia County     | $535,900            | Conventional  |
| Wisconsin    | St. Croix County  | $326,600            | Conventional  |

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
    And I select <county_name> County
    And I change to "<new_loan_type>" Loan Type
  Then I should see the chart active with new data
    But I should NOT see the County selection

Examples:
| state_name   | county_name       | FHA_max_loan_amount | new_loan_type |
| Georgia      | Cobb County       | $342,700            | VA            |
| Illinois     | Kane County       | $365,700            | VA            |
| Maryland     | Baltimore city    | $517,500            | VA            |
| New Jersey   | Monmouth County   | $625,500            | VA            |
| Oregon       | Hood River County | $371,450            | VA            |
| Pennsylvania | Lehigh County     | $372,600            | VA            |
| Virginia     | Amelia County     | $535,900            | VA            |
| Wisconsin    | St. Croix County  | $322,000            | VA            |
| Georgia      | Cobb County       | $342,700            | Conventional  |
| Illinois     | Kane County       | $365,700            | Conventional  |
| Maryland     | Baltimore city    | $517,500            | Conventional  |
| New Jersey   | Monmouth County   | $625,500            | Conventional  |
| Oregon       | Hood River County | $371,450            | Conventional  |
| Pennsylvania | Lehigh County     | $372,600            | Conventional  |
| Virginia     | Amelia County     | $535,900            | Conventional  |
| Wisconsin    | St. Croix County  | $322,000            | Conventional  |
