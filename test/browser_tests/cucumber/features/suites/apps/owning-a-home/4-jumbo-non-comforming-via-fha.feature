Feature: Test 4: Triggering non-conforming jumbo via FHA - Purpose: This test looks for correct behavior in triggering a jumbo (non-conforming) loan when FHA high balance is not available.
  As a first time visitor to the Rate Checker page
  I want to see Jumbo non-conforming alerts
  So that I can make informed choices when shopping for an FHA loan

Background:
  Given I navigate to the "Rate Checker" page

@jumbo
Scenario Outline: Trigger conforming jumbo loan
  When I select "<state_name>" as State
    And I select "FHA" Loan Type
    And I enter "20" as Down Payment percent
    And I enter $"550,000" as House Price amount
  Then I should see the chart faded out to indicate the data is out of date
    And I should see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    And I should see the County field highlighted

Examples:
| state_name   |
| Kansas       |
| Louisiana    |
| Michigan     |
| New Mexico   |
| North Dakota |
| Oklahoma     |

@jumbo
Scenario Outline: Trigger non-conforming jumbo loan
  When I select "<state_name>" as State
    And I select "FHA" Loan Type
    And I enter "20" as Down Payment percent
    And I enter $"550,000" as House Price amount
    And I select <county_name> County
  Then I should see the chart active with new data
    And I should see "Jumbo (non-conforming)" as the selected Loan Type
    And I should see the Loan Type field highlighted
    And I should see an HB alert "You are not eligible for an FHA loan when you borrow more than <FHA_max_loan_amount> in your county. The only loan type available to you at this loan amount is a jumbo (non-conforming) loan."
    But I should NOT see a County alert "Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates."
    But I should NOT see the County field highlighted

Examples:
| state_name   | county_name       | FHA_max_loan_amount |
| Kansas       | Sherman County    | $275,665            |
| Louisiana    | Iberville Parish  | $275,665            |
| Michigan     | Kalamazoo County  | $275,665            |
| New Mexico   | Los Alamos County | $380,650            |
| North Dakota | Billings County   | $339,250            |
| Oklahoma     | Cotton County     | $275,665            |
