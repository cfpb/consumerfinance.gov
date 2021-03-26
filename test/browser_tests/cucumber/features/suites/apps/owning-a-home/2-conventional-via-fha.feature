Feature: Test 2: Triggering conventional via FHA
  As a first time visitor to the Rate Checker page
  I want to see FHA High Balance alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@high_balance @hp_first
Scenario Outline: Triggering a Conventional loan when FHA high balance is not available
  When I select "<state_name>" as State
    And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name |
| Alabama    |
| Arizona    |
| Colorado   |
| Florida    |
| Indiana    |
| Utah       |
| Kansas     |
| Montana    |

@high_balance @hp_first
Scenario Outline: Triggering a Conventional loan when FHA high balance is not available
  When I select "<state_name>" as State
    And I enter $"350,000" as House Price amount
    And I select "FHA" Loan Type
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "Conventional" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "You are not eligible for an FHA loan when you borrow more than <FHA_max_loan_amount> in your county. You are eligible for a conventional loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    But I should NOT see the County field highlighted

 Examples:
| state_name | county_name       | FHA_max_loan_amount |
| Alabama    | Bibb County       | $275,665            |
| Arizona    | Apache County     | $275,665            |
| Colorado   | Morgan County     | $275,665            |
| Florida    | Okeechobee County | $275,665            |
| Indiana    | Monroe County     | $275,665            |
| Utah       | Salt Lake County  | $312,800            |
| Kansas     | Johnson County    | $278,300            |
| Montana    | Missoula County   | $289,800            |

@high_balance @lt_first
Scenario Outline: Triggering a Conventional loan when FHA high balance is not available
  When I select "<state_name>" as State
    And I select "FHA" Loan Type
    And I enter $"350,000" as House Price amount
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name |
| Alabama    |
| Arizona    |
| Colorado   |
| Florida    |
| Indiana    |
| Utah       |
| Kansas     |
| Montana    |

@high_balance @lt_first
Scenario Outline: Triggering a Conventional loan when FHA high balance is not available
  When I select "<state_name>" as State
    And I select "FHA" Loan Type
    And I enter $"350,000" as House Price amount
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "Conventional" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "You are not eligible for an FHA loan when you borrow more than <FHA_max_loan_amount> in your county. You are eligible for a conventional loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    But I should NOT see the County field highlighted

 Examples:
| state_name | county_name       | FHA_max_loan_amount |
| Alabama    | Bibb County       | $275,665            |
| Arizona    | Apache County     | $275,665            |
| Colorado   | Morgan County     | $275,665            |
| Florida    | Okeechobee County | $275,665            |
| Indiana    | Monroe County     | $275,665            |
| Utah       | Salt Lake County  | $312,800            |
| Kansas     | Johnson County    | $278,300            |
| Montana    | Missoula County   | $289,800            |
