Feature: Test 7: Changing loan types - Purpose: check for correct behavior when you change the loan type before choosing a county after triggering FHA HB
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance
Scenario Outline: Triggering FHA high-balance
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
Scenario Outline: Changing Loan Type
  When I select "<state_name>" as State
    And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
    And I change to "<new_loan_type>" Loan Type
  Then I should see the chart active with new data
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
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
| Wisconsin    | St. Croix County  | $326,600            | VA            |
| Georgia      | Cobb County       | $342,700            | Conventional  |
| Illinois     | Kane County       | $365,700            | Conventional  |
| Maryland     | Baltimore city    | $517,500            | Conventional  |
| New Jersey   | Monmouth County   | $625,500            | Conventional  |
| Oregon       | Hood River County | $371,450            | Conventional  |
| Pennsylvania | Lehigh County     | $372,600            | Conventional  |
| Virginia     | Amelia County     | $535,900            | Conventional  |
| Wisconsin    | St. Croix County  | $326,600            | Conventional  |
