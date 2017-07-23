Feature: Negative tests for the rate checker API 
  As an API client
  I want to query the Rate Checker API
  So that I can ensure that the errors codes are returned properly when a parameter is required

@smoke_testing
Scenario Outline: Omit the House Price parameter
        Given I omit the "<parameter_name>" field
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>" 
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "price" is required

  Examples:
  | parameter_name | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type |
  | House Price    | 180000      | 700     | 720     | AL    | fixed          | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Loan Amount parameter
        Given I select "<house_price>" as House Price
          And I omit the "<parameter_name>" field
          And I select my minimum credit score as "<minfico>" 
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "loan_amount" is required

  Examples:
  | parameter_name | house_price | minfico | maxfico | state | rate_structure | loan_term | loan_type | arm_type |
  | Loan Amount    | 200000      | 700     | 720     | AL    | fixed          | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Minimum Credit Score parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I omit the "<parameter_name>" field 
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "minfico" is required

  Examples:
  | parameter_name        | house_price | loan_amount | maxfico | state | rate_structure | loan_term | loan_type | arm_type |
  | Minimum Credit Score  | 200000      | 180000      | 720     | AL    | fixed          | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Maximum Credit Score parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I omit the "<parameter_name>" field 
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "maxfico" is required

  Examples:
  | parameter_name        | house_price | loan_amount | minfico | state | rate_structure | loan_term | loan_type | arm_type |
  | Maximum Credit Score  | 200000      | 180000      | 700     | AL    | fixed          | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the State parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I omit the "<parameter_name>" field
          And I select "<rate_structure>" as Rate Structure 
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "state" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | rate_structure | loan_term | loan_type | arm_type |
  | State           | 200000      | 180000      | 700     | 720     | fixed          | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Rate Structure parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I omit the "<parameter_name>" field 
          And I select "<loan_term>" as Loan Term
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "rate_structure" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | loan_term | loan_type | arm_type |
  | Rate Structure  | 200000      | 180000      | 700     | 720     | NV    | 30        | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Loan Term parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure 
          And I omit the "<parameter_name>" field 
          And I select "<loan_type>" as Loan Type
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "loan_term" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_type | arm_type |
  | Loan Term       | 200000      | 180000      | 700     | 720     | NV    | fixed          | conf      | 3-1      |

@smoke_testing
Scenario Outline: Omit the Loan Type parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term 
          And I omit the "<parameter_name>" field 
          And I select "<arm_type>" as ARM Type 
        When I send the request
        Then the response should state that required parameter "loan_type" is required

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | arm_type |
  | Loan Type       | 200000      | 180000      | 700     | 720     | NV    | fixed          | 30        | 3-1      |

@smoke_testing @prod_only
Scenario Outline: Omit the ARM Type parameter
        Given I select "<house_price>" as House Price
          And I select "<loan_amount>" as Loan Amount
          And I select my minimum credit score as "<minfico>"
          And I select my maximum credit score as "<maxfico>"
          And I select "<state>" as State
          And I select "<rate_structure>" as Rate Structure
          And I select "<loan_term>" as Loan Term 
          And I select "<loan_type>" as Loan Type
          And I omit the "<parameter_name>" field  
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | parameter_name  | house_price | loan_amount | minfico | maxfico | state | rate_structure | loan_term | loan_type |
  | ARM Type        | 200000      | 180000      | 700     | 720     | NV    | arm            | 30        | conf      |
