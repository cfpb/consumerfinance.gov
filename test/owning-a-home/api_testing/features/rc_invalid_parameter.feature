Feature: Negative tests for the rate checker API 
  As an API client
  I want to query the Rate Checker API
  So that I can ensure that the errors codes are returned properly when a parameter is missing

@smoke_testing @prod_only
Scenario Outline: Send invalid house price
        Given I select "<invalid_house_price>" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_house_price   	|
  | a&b\n           		|
  | 999,999,999,999,999     |

@smoke_testing @prod_only
Scenario Outline: Send invalid Loan Amount
        Given I select "200000" as House Price
          And I select "<invalid_loan_amount>" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_amount   	|
  | %*@ !# ^%          		|
  | 999,999,999,999,999     |
  | AbCd   				    |

@smoke_testing @prod_only
Scenario Outline: Send invalid minimum credit score
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "<invalid_minfico>" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_minfico     	|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid maximum credit score
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "<invalid_maxfico>"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_maxfico     	|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid State
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "<invalid_state>" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_state       	|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid Rate Structure
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "<invalid_rate_structure>" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_rate_structure  |
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | AbCd                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid Loan Term
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "<invalid_loan_term>" as Loan Term
          And I select "conf" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_term  		|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | AbCd                    |
  | -1.2                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid Loan Type
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "<invalid_loan_type>" as Loan Type
          And I select "3-1" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_loan_type  		|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | VA bCd                  |
  | -1.2                    |

@smoke_testing @prod_only
Scenario Outline: Send invalid ARM Type
        Given I select "200000" as House Price
          And I select "180000" as Loan Amount
          And I select my minimum credit score as "700" 
          And I select my maximum credit score as "720"
          And I select "AL" as State
          And I select "fixed" as Rate Structure
          And I select "30" as Loan Term
          And I select "conf" as Loan Type
          And I select "<invalid_ARM_type>" as ARM Type 
        When I send the request
        Then the response should NOT include "Traceback"

  Examples:
  | invalid_ARM_type 		|
  | %*@ !# ^%            	|
  | 999,999,999,999,999     |
  | VA bCd                  |
  | -1.2 					|
