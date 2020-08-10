Feature: Verify that Rate Checker fields default to the correct values
  As a first time visitor to the Rate Checker page
  I want to have some fields pre-populated
  So that I can make informed choices when shopping for a mortgage loan

Background:
  Given I navigate to the "Rate Checker" page


@smoke_testing @rate_checker
Scenario: Default credit score range
  Then I should see the Credit Score Range displayed as "700 - 719"


@smoke_testing @rate_checker
Scenario: Default location
  Then I should see "District of Columbia" as the selected location


@smoke_testing @rate_checker
Scenario: Default House price
  Then I should see $"200,000" as the House price


@smoke_testing @rate_checker
Scenario: Default Down Payment amount
  Then I should see $"20,000" as Down Payment amount


@smoke_testing @rate_checker
Scenario: Default Down Payment percent
  Then I should see "10" as Down Payment percent


@smoke_testing @rate_checker
Scenario: Default loan amount
  Then I should see "$180,000" as Loan Amount


@smoke_testing @rate_checker
Scenario: Default Rate Structure
  Then I should see "Fixed" as the selected Rate Structure


@smoke_testing @rate_checker
Scenario: Deafult ARM Type
  When I select "Adjustable" Rate Structure
  Then I should see "5/1" as the selected ARM Type


@smoke_testing @rate_checker
Scenario: Default Loan Term
  Then I should see "30 Years" as the selected Loan Term


@smoke_testing @rate_checker
Scenario: Default Loan Type
  Then I should see "Conventional" as the selected Loan Type


@smoke_testing @rate_checker
Scenario: Default tab
  Then I should see the "I plan to buy in the next couple of months" tab selected


@smoke_testing @rate_checker
Scenario: County should NOT be visible by default
  Then I should NOT see the County selection


@smoke_testing @rate_checker
Scenario: ARM Type should NOT be visible by default
  Then I should NOT see the ARM Type selection
