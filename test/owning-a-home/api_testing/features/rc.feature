Feature: Test the rate checker API
  As an API client
  I want to query the Rate Checker API
  So that I can ensure that the data is returned properly

@smoke_testing
Scenario Outline: Verify the API response includes a timestamp and data field
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type
        When I send the request
        Then the response should include a timestamp field
          And the response should include a data field

  Examples:
  | house_price   | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type  | arm_type |
  # 30 year fixed (minfico, maxfico scores)
  | 200000        | 180000      | 840     | 850     | AL    | fixed          | 30        | conf       | 5-1      |
  | 200000        | 180000      | 620     | 639     | AL    | fixed          | 30        | conf       | 5-1      |
  | 200000        | 180000      | 700     | 719     | AL    | fixed          | 30        | conf       | 5-1      |
  # 15 year fixed (minfico, maxfico scores)
  | 200000        | 180000      | 840     | 850     | AL    | fixed          | 15        | conf       | 5-1      |
  | 200000        | 180000      | 620     | 639     | AL    | fixed          | 15        | conf       | 5-1      |
  | 200000        | 180000      | 700     | 719     | AL    | fixed          | 15        | conf       | 5-1      |
  # 30 year fixed (Conventional, FHA and VA)
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 30        | conf       | 5-1      |
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 30        | fha        | 5-1      |
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 30        | va         | 5-1      |
  # 15 year fixed (Conventional, FHA and VA)
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 15        | conf       | 5-1      |
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 15        | fha        | 5-1      |
  | 200000        | 180000      | 700     | 720     | AL    | fixed          | 15        | va         | 5-1      |
  # ARM (3-1, 5-1, 7-1, 10-1)
  | 200000        | 180000      | 700     | 720     | AL    | arm            | 30        | conf       | 3-1      |
  | 200000        | 180000      | 700     | 720     | AL    | arm            | 30        | conf       | 5-1      |
  | 200000        | 180000      | 700     | 720     | AL    | arm            | 30        | conf       | 7-1      |
  | 200000        | 180000      | 700     | 720     | AL    | arm            | 30        | conf       | 10-1     |
  # CONVENTIONAL (CONFORMING), CONFORMING JUMBO and JUMBO (NON-CONFORMING)
  | 521250        | 424100      | 700     | 720     | AL    | fixed          | 30        | va         | 5-1      |
  | 550000        | 440000      | 700     | 720     | AL    | fixed          | 30        | jumbo      | 5-1      |
  | 1550000       | 1240000     | 700     | 720     | AL    | fixed          | 30        | jumbo      | 5-1      |
