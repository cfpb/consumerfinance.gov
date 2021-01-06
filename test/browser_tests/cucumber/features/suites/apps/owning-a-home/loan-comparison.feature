Feature: Test the default values in the Loan Comparison page
  As a first time visitor to the Owning a Home page
  I want to have fields pre-poluated
  So that I can compare loan costs easily

Background:
  Given I navigate to the "Loan Comparison" page

@loan_comparison
Scenario: Test inbound links in the Loan Options page
  When I click on the "Check out the Rate Checker" link
  Then I should be directed to the internal "rate-checker" URL
