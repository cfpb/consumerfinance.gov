Feature: Verify the Loan Options page defaults to the correct values
  As a first time visitor to the Loan Options page
  I want to have certain fields pre-populated
  So that I can find the information I'm looking for

Background:
  Given I navigate to the "Loan Options" page

@smoke_testing @loan_options @loan_options_expandable
Scenario: Click 'Learn More' to expand sections
  When I click Learn More to expand the "Loan term" section
  Then I should see "$200,000" as the default loan amount
    And I should see "5%" as the default interest rate
      And I should see "30" years as the default loan term
