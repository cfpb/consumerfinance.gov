Feature: Test the mortgage insurance API
  As an API client
  I want to query the Mortgage Insurance API
  So that I can ensure that the data is returned properly

@smoke_testing
Scenario Outline: Verify the API response includes a data field
        Given I select "<mortgage_house_price>" as Mortgage Insurance House Price
          And I select "<mortgage_loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<mortgage_minfico>"
          And I select my mortgage insurance maximum credit score as "<mortgage_maxfico>"
          And I select "<mortgage_rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<mortgage_loan_term>" as Mortgage Insurance Loan Term
          And I select "<mortgage_loan_type>" as Mortgage Insurance Loan Type
          And I select "<mortgage_arm_type>" as Mortgage Insurance ARM Type
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a data field

  Examples:
  | mortgage_house_price   | mortgage_loan_amount | mortgage_minfico | mortgage_maxfico | mortgage_rate_structure | mortgage_loan_term | mortgage_loan_type  | mortgage_arm_type | va_status | va_first_use |
  # 30 year fixed (minfico, maxfico scores)
  | 200000        | 180000      | 840     | 850     | fixed          | 30        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 620     | 639     | fixed          | 30        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 719     | fixed          | 30        | conf       | 5-1      | regular   | 1            |
  # 15 year fixed (minfico, maxfico scores)
  | 200000        | 180000      | 840     | 850     | fixed          | 15        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 620     | 639     | fixed          | 15        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 719     | fixed          | 15        | conf       | 5-1      | regular   | 1            |
  # 30 year fixed (Conventional, FHA and VA)
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | fha        | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | disabled  | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | res-ng    | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | regular   | 0            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | disabled  | 0            |
  | 200000        | 180000      | 700     | 720     | fixed          | 30        | va         | 5-1      | res-ng    | 0            |
  # 15 year fixed (Conventional, FHA and VA)
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | fha        | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | disabled  | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | res-ng    | 1            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | regular   | 0            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | disabled  | 0            |
  | 200000        | 180000      | 700     | 720     | fixed          | 15        | va         | 5-1      | res-ng    | 0            |
  # ARM (5-1, 7-1, 10-1)
  | 200000        | 180000      | 700     | 720     | arm            | 30        | conf       | 5-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | arm            | 30        | conf       | 7-1      | regular   | 1            |
  | 200000        | 180000      | 700     | 720     | arm            | 30        | conf       | 10-1     | regular   | 1            |
  # CONVENTIONAL (CONFORMING), CONFORMING JUMBO and JUMBO (NON-CONFORMING)
  | 521250        | 424100      | 700     | 720     | fixed          | 30        | va         | 5-1      | regular   | 1            |
  | 550000        | 440000      | 700     | 720     | fixed          | 30        | jumbo      | 5-1      | regular   | 1            |
  | 1550000       | 1240000     | 700     | 720     | fixed          | 30        | jumbo      | 5-1      | regular   | 1            |
