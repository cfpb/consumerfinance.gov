Feature: Negative tests for the mortgage insurance API 
  As an API client
  I want to query the Mortgage Insurance API
  So that I can ensure that the errors codes are returned properly when a parameter is invalid

@smoke_testing 
Scenario Outline: Send invalid house price
        Given I select "<invalid_house_price>" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use 
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "price" field
        Then the mortgage insurance response should NOT include "Traceback"

  Examples:
  | invalid_house_price     |
  | a&b\n                   |
  | 999,999,999,999,999     |
  | 0                       |

@smoke_testing
Scenario Outline: Send invalid loan amount
        Given I select "200000" as Mortgage Insurance House Price
          And I select "<invalid_loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "loan_amount" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_amount     |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing
Scenario Outline: Send invalid minimum credit score
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<invalid_minfico>" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "minfico" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_minfico         |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing
Scenario Outline: Send invalid maximum credit score
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "<invalid_maxfico>"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "maxfico" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_maxfico         |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | AbCd                    |


@smoke_testing
Scenario Outline: Send invalid Rate Structure
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "<invalid_rate_structure>" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "rate_structure" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_rate_structure  |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing
Scenario Outline: Send invalid Loan Term
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "<invalid_loan_term>" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "loan_term" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_term       |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | AbCd                    |
  | -1.2                    |

@smoke_testing
Scenario Outline: Send invalid Loan Type
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "<invalid_loan_type>" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "loan_type" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_type       |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | VA bCd                  |
  | -1.2                    |

@smoke_testing
Scenario Outline: Send invalid ARM Type
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "<invalid_ARM_type>" as Mortgage Insurance ARM Type 
          And I select "regular" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "arm_type" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_ARM_type        |
  | %*@ !# ^%               |
  | 999,999,999,999,999     |
  | VA bCd                  |
  | -1.2                    |

@smoke_testing
Scenario Outline: Send invalid VA Status
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type 
          And I select "<invalid_va_status>" as VA Status
          And I select "n" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "va_status" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_va_status        |
  | %*@ !# ^%                |
  | 999,999,999,999,999      |
  | VA bCd                   |
  | -1.2                     |

@smoke_testing
Scenario Outline: Send invalid First Time VA Loan Use
        Given I select "200000" as Mortgage Insurance House Price
          And I select "180000" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "700" 
          And I select my mortgage insurance maximum credit score as "720"
          And I select "fixed" as Mortgage Insurance Rate Structure
          And I select "30" as Mortgage Insurance Loan Term
          And I select "conf" as Mortgage Insurance Loan Type
          And I select "5-1" as Mortgage Insurance ARM Type 
          And I select "regular" as VA Status
          And I select "<invalid_va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include a "va_first_use" field
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_va_first_use        |
  | %*@ !# ^%                   |
  | 999,999,999,999,999         |
  | VA bCd                      |
  | -1.2                        |
