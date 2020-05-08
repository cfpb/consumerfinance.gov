Feature: Test 5: Triggering conventional via FHA high-balance + increase in house price - Purpose: This test looks for correct behavior in triggering a conventional loan, via an FHA high-balance loan and an increase in house price
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I enter $"310,000" as House Price amount
    And I select "FHA" Loan Type
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name   |
| Georgia      |
| Illinois     |
| Oregon       |
| Pennsylvania |
| Wisconsin    |
| New Mexico   |
| North Dakota |
| Connecticut  |

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance
  When I select "<state_name>" as State
    And I enter $"310,000" as House Price amount
    And I select "FHA" Loan Type
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see "FHA high-balance" as the selected Loan Type
    And I should see an HB alert "When you borrow between $275,665 and <FHA_max_loan_amount> in your county, you are eligible for a high-balance FHA loan."

Examples:
| state_name   | county_name       | FHA_max_loan_amount |
| Georgia      | Cobb County       | $342,700            |
| Illinois     | Kane County       | $365,700            |
| Oregon       | Hood River County | $371,450            |
| Pennsylvania | Lehigh County     | $372,600            |
| Wisconsin    | St. Croix County  | $326,600            |
| New Mexico   | Los Alamos County | $380,650            |
| North Dakota | Billings County   | $339,250            |
| Connecticut  | Middlesex County  | $353,050            |

@high_balance
Scenario Outline: Triggering conventional via FHA high-balance + increase in house price
  When I select "<state_name>" as State
    And I enter $"310,000" as House Price amount
    And I select "FHA" Loan Type
    And I select <county_name> County
    And I change the House Price amount to $"450,000"
  Then I should see the chart active with new data
    And I should see "Conventional" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "You are not eligible for an FHA loan when you borrow more than <FHA_max_loan_amount> in your county. You are eligible for a conventional loan."
    But I should NOT see the County field highlighted

Examples:
| state_name   | county_name       | FHA_max_loan_amount |
| Georgia      | Cobb County       | $342,700            |
| Illinois     | Kane County       | $365,700            |
| Oregon       | Hood River County | $371,450            |
| Pennsylvania | Lehigh County     | $372,600            |
| Wisconsin    | St. Croix County  | $326,600            |
| New Mexico   | Los Alamos County | $380,650            |
| North Dakota | Billings County   | $339,250            |
| Connecticut  | Middlesex County  | $353,050            |
