Feature: Test the Loan Amount calculations
  As a first time visitor to the Rate Checker page
  I want to enter house price and interest rate
  So that I can estimate my loan amount

Background:
  Given I navigate to the "Rate Checker" page


@rate_checker
Scenario Outline: Calculate loan amount based on house price and down payment amount
  When I enter $"<house_price>" as House Price amount
    And I enter $"<down_payment_amount>" as Down Payment amount
  Then I should see "<loan_amount>" as Loan Amount

Examples:
| house_price | down_payment_amount | loan_amount |
| 100,000     | 20,000              | $80,000     |
| 250,000     | 42,500              | $207,500    |
| 780,000     | 68,640              | $711,360    |
| 1,250,000   | 187,500             | $1,062,500  |
| 200,000     | 20,000              | $180,000    |


@rate_checker
Scenario Outline: Calculate down payment amount based on house price and down payment percent
  When I enter $"<house_price>" as House Price amount
    And I enter "<down_payment_percent>" as Down Payment percent
  Then I should see $"<down_payment_amount>" as Down Payment amount

Examples:
| house_price | down_payment_percent | down_payment_amount |
| 250,000     | 17                   | 42500               |
| 100,000     | 20                   | 20000               |
| 780,000     | 9                    | 70200               |
| 1,250,000   | 15                   | 187500              |
| 200,000     | 10                   | 20000               |


@rate_checker
Scenario Outline: Calculate down payment percent based on house price and down payment amount
  When I enter $"<house_price>" as House Price amount
    And I enter $"<down_payment_amount>" as Down Payment amount
  Then I should see "<down_payment_percent>" as Down Payment percent

Examples:
| house_price | down_payment_amount | down_payment_percent |
| 100,000     | 15000               | 15                   |
| 150,000     | 6000                | 4                    |
| 780,000     | 70200               | 9                    |
| 1,250,000   | 237500              | 19                   |


@rate_checker
Scenario Outline: Enter then modify down payment percent
  When I enter $"<house_price>" as House Price amount
    And I enter "<initial_percent>" as Down Payment percent
    And I change the Down Payment percent to "<modified_percent>"
  Then I should see $"<down_payment_amount>" as Down Payment amount

Examples:
| house_price | initial_percent | modified_percent | down_payment_amount |
| 100,000     | 10              | 20               | 20000               |
| 250,000     | 30              | 15               | 37500               |


@rate_checker
Scenario Outline: Modify down payment amount
  When I enter $"<house_price>" as House Price amount
    And I enter "<initial_percent>" as Down Payment percent
    And I change the Down Payment amount to $"<modified_dp_amount>"
  Then I should see the chart active with new data
    And I should see "<modified_percent>" as Down Payment percent

Examples:
| house_price | initial_percent | modified_dp_amount | modified_percent |
| 100,000     | 10              | 9000               | 9                |
| 250,000     | 15              | 40000              | 16               |
| 350,000     | 17              | 50000              | 14               |


@rate_checker
Scenario Outline: Modify Down Payment amount then modify the House Price
  When I enter $"<house_price>" as House Price amount
    And I enter "<initial_percent>" as Down Payment percent
    And I change the Down Payment amount to $"<modified_dp_amount>"
    And I change the House Price amount to $"<modified_house_price>"
  Then I should see the chart active with new data
    And I should see "<modified_percent>" as Down Payment percent

Examples:
| house_price | initial_percent | modified_dp_amount | modified_house_price | modified_percent |
| 100,000     | 10              | 9000               | 175000               | 5                |
| 250,000     | 12              | 45000              | 275000               | 16               |


@rate_checker
Scenario Outline: Modify Down Payment percent then modify the House Price
  When I enter $"<house_price>" as House Price amount
    And I enter "<initial_percent>" as Down Payment percent
    And I change the Down Payment percent to "<modified_percent>"
    And I change the House Price amount to $"<modified_house_price>"
  Then I should see the chart active with new data
    And I should see $"<modified_dp_amount>" as Down Payment amount

Examples:
| house_price | initial_percent | modified_dp_amount | modified_house_price | modified_percent |
| 100000      | 10              | 35000              | 175000               | 20               |
| 250000      | 12              | 36000              | 225000               | 16               |


@rate_checker
Scenario Outline: Attempt to enter invalid characters as House Price
  When I enter $"<invalid_characters>" as House Price amount
  Then I should see $"<hp_amount>" as the House price

Examples:
| invalid_characters | hp_amount |
| 2&5*0!000          | 250000    |
| 1@@2##5000         | 125000    |


@rate_checker
Scenario Outline: Attempt to enter invalid characters as House Price
  When I enter $"<invalid_characters>" as House Price amount
  Then I should see a DP alert "Your down payment cannot be more than your house price."

Examples:
| invalid_characters |
| 0                  |
| zzzz               |
| @#$%^&*()          |
| -                  |


@rate_checker
Scenario Outline: Attempt to enter invalid characters as House Price
  When I enter $"<house_price>" as House Price amount
    And I enter $"<down_payment_amount>" as Down Payment amount
  Then I should see a DP alert "Your down payment cannot be more than your house price."

Examples:
| house_price | down_payment_amount |
| 20000       | 25000               |
| 15000       | 15001               |
| 0           | 1                   |
