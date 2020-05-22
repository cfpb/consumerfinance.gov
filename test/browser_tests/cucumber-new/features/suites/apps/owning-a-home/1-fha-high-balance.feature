Feature: Test 1: Triggering FHA-high balance - Purpose: This test looks for correct behavior in triggering an FHA high-balance situation.
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page


@fha_high_balance @hp_first
Scenario Outline: Trigger the County warning
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


@fha_high_balance @hp_first
Scenario Outline: Triggering FHA High Balance loan warning
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
| state_name   | county_name       | FHA_max_loan_amount |
| Georgia      | Cobb County       | $342,700            |
| Illinois     | Kane County       | $365,700            |
| Maryland     | Baltimore city    | $517,500            |
| New Jersey   | Monmouth County   | $625,500            |
| Oregon       | Hood River County | $371,450            |
| Pennsylvania | Lehigh County     | $372,600            |
| Virginia     | Amelia County     | $535,900            |
| Wisconsin    | St. Croix County  | $326,600            |


@fha_high_balance @lt_first
Scenario Outline: Trigger the County warning
  When I select "<state_name>" as State
    And I select "FHA" Loan Type
    And I enter $"350,000" as House Price amount
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


@fha_high_balance @lt_first
Scenario Outline: Triggering FHA High Balance loan warning
  When I select "<state_name>" as State
  And I select "FHA" Loan Type
  And I enter $"350,000" as House Price amount
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "FHA high-balance" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "When you borrow between $275,665 and <FHA_max_loan_amount> in your county, you are eligible for a high-balance FHA loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
  But I should NOT see the County field highlighted

Examples:
| state_name   | county_name       | FHA_max_loan_amount |
| Georgia      | Cobb County       | $342,700            |
| Illinois     | Kane County       | $365,700            |
| Maryland     | Baltimore city    | $517,500            |
| New Jersey   | Monmouth County   | $625,500            |
| Oregon       | Hood River County | $371,450            |
| Pennsylvania | Lehigh County     | $372,600            |
| Virginia     | Amelia County     | $535,900            |
| Wisconsin    | St. Croix County  | $326,600            |
