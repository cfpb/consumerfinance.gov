Feature: Negative tests for the mortgage insurance API 
  As an API client
  I want to query the Mortgage Insurance API
  So that I can ensure that the errors codes are returned properly when a parameter is missing

@smoke_testing
Scenario Outline: Omit the House Price parameter
        Given I omit the mortgage insurance "<parameter_name>" field
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>" 
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "price" is required

  Examples:
  | parameter_name | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type | va_status | va_first_use |
  | House Price    | 180000      | 700     | 720     | AL    | fixed          | 30        | conf      | 5-1      | regular   | 0            |

@smoke_testing
Scenario Outline: Omit the Loan Amount parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I omit the mortgage insurance "<parameter_name>" field
          And I select my mortgage insurance minimum credit score as "<minfico>" 
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "loan_amount" is required

  Examples:
  | parameter_name | house_price | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type | va_status | va_first_use |
  | Loan Amount    | 200000      | 700     | 720     | AL    | fixed          | 30        | conf      | 5-1      | regular   | 0            |

@smoke_testing
Scenario Outline: Omit the Minimum Credit Score parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I omit the mortgage insurance "<parameter_name>" field 
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "minfico" is required

  Examples:
  | parameter_name        | house_price | loan_amount | maxfico | state | rate_structure | loan_term | loan_type | arm_type | va_status | va_first_use |
  | Minimum Credit Score  | 200000      | 180000      | 720     | AL    | fixed          | 30        | conf      | 5-1      | regular   | 0            |


@smoke_testing
Scenario Outline: Omit the Maximum Credit Score parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I omit the mortgage insurance "<parameter_name>" field 
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "maxfico" is required

  Examples:
  | parameter_name        | house_price | loan_amount | minfico | state | rate_structure | loan_term | loan_type | arm_type | va_status | va_first_use |
  | Maximum Credit Score  | 200000      | 180000      | 700     | AL    | fixed          | 30        | conf      | 5-1      | regular   | 0            |  


@smoke_testing
Scenario Outline: Omit the Rate Structure parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I omit the mortgage insurance "<parameter_name>" field 
          And I select "<loan_term>" as Mortgage Insurance Loan Term
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "rate_structure" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | loan_term | loan_type | arm_type | va_status | va_first_use |
  | Rate Structure  | 200000      | 180000      | 700     | 720     | NV    | 30        | conf      | 5-1      | regular   | 0            |  

@smoke_testing
Scenario Outline: Omit the Loan Term parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure 
          And I omit the mortgage insurance "<parameter_name>" field 
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "loan_term" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_type | arm_type | va_status | va_first_use |
  | Loan Term       | 200000      | 180000      | 700     | 720     | NV    | fixed          | conf      | 5-1      | regular   | 0            |  

@smoke_testing
Scenario Outline: Omit the Loan Type parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term 
          And I omit the mortgage insurance "<parameter_name>" field 
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should state that required parameter "loan_type" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | arm_type | va_status | va_first_use |
  | Loan Type       | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | 5-1      | regular   | 0            |

@smoke_testing
Scenario Outline: Omit the ARM Type parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term 
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I omit the mortgage insurance "<parameter_name>" field  
          And I select "<va_status>" as VA Status
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include error stating "arm_type is required if rate_structure is ARM"

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type | va_status | va_first_use |
  | ARM Type        | 200000      | 180000      | 700     | 720     | NV    | arm            | 30        | conf      | regular   | 0            |

@smoke_testing
Scenario Outline: Omit the VA Status parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term 
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type 
          And I omit the mortgage insurance "<parameter_name>" field
          And I select "<va_first_use>" as First Time VA Loan Use
        When I send the mortgage insurance request
        Then the mortgage insurance response should include error stating "va_status is required if loan_type is VA or VA-HB"

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type | va_first_use |
  | VA Status       | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | va        | 5-1      | 0            |
  | VA Status       | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | va-hb     | 5-1      | 0            |

@smoke_testing @amy
Scenario Outline: Omit the VA First Use parameter
        Given I select "<house_price>" as Mortgage Insurance House Price
          And I select "<loan_amount>" as Mortgage Insurance Loan Amount
          And I select my mortgage insurance minimum credit score as "<minfico>"
          And I select my mortgage insurance maximum credit score as "<maxfico>"
          And I select "<rate_structure>" as Mortgage Insurance Rate Structure
          And I select "<loan_term>" as Mortgage Insurance Loan Term 
          And I select "<loan_type>" as Mortgage Insurance Loan Type
          And I select "<arm_type>" as Mortgage Insurance ARM Type  
          And I select "<va_status>" as VA Status
          And I omit the mortgage insurance "<parameter_name>" field
        When I send the mortgage insurance request
        Then the mortgage insurance response should include error stating "va_first_use is required if va_status is not DISABLED"

  Examples:
  | parameter_name         | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type | va_status |
  | First Time VA Loan Use | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | va        | 5-1      | regular   |
  | First Time VA Loan Use | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | va-hb     | 5-1      | RES-NG    |



